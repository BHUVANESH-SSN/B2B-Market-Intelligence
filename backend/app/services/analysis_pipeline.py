from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import select

from app.db.crud.competitor import get_competitor_by_id
from app.db.crud.job import get_job_by_id
from app.db.crud.report import create_report
from app.db.models import Diff, Insight, Job, Snapshot
from app.db.models.enums import JobStatus
from app.db.session import SessionLocal
from app.services.ai_agent_client import AIAgentIntegrationError, request_agent_analysis
from app.services.redis_state import invalidate_insights_cache, set_job_status

logger = logging.getLogger(__name__)


def process_analysis_job(job_id: str) -> dict[str, Any]:
    session = SessionLocal()
    parsed_job_id = UUID(job_id)

    try:
        job = _get_job_or_raise(session, parsed_job_id)
        request_payload = dict((job.details or {}).get("request") or {})

        competitor_id = request_payload.get("competitor_id")
        if not competitor_id:
            raise ValueError("Analysis job is missing competitor_id.")

        competitor = get_competitor_by_id(session, competitor_id=UUID(competitor_id))
        if competitor is None:
            raise ValueError("Competitor not found for analysis.")

        job.status = JobStatus.RUNNING
        session.commit()
        set_job_status(job_id=job.id, status=JobStatus.RUNNING.value, progress=10, step="fetch_competitor")

        previous_snapshot = session.scalar(
            select(Snapshot)
            .where(Snapshot.competitor_id == competitor.id)
            .order_by(Snapshot.created_at.desc())
            .limit(1)
        )

        snapshot_content = _build_snapshot_content(
            competitor_name=competitor.name,
            competitor_domain=competitor.domain,
            prompt=request_payload.get("prompt"),
        )
        new_snapshot = Snapshot(
            competitor_id=competitor.id,
            content=snapshot_content,
            content_hash=hashlib.sha256(snapshot_content.encode("utf-8")).hexdigest(),
            storage_path=None,
        )
        session.add(new_snapshot)
        session.flush()
        set_job_status(job_id=job.id, status=JobStatus.RUNNING.value, progress=30, step="snapshot_stored")

        diff_text = _build_diff_text(previous_snapshot.content if previous_snapshot else None, snapshot_content)
        diff = Diff(
            competitor_id=competitor.id,
            old_snapshot_id=previous_snapshot.id if previous_snapshot else None,
            new_snapshot_id=new_snapshot.id,
            diff_text=diff_text,
        )
        session.add(diff)
        session.flush()
        set_job_status(job_id=job.id, status=JobStatus.RUNNING.value, progress=55, step="diff_generated")

        generated = _generate_analysis_bundle(
            competitor_name=competitor.name,
            competitor_domain=competitor.domain,
            request_payload=request_payload,
            diff_text=diff_text,
        )

        insight_ids: list[str] = []
        for item in generated["insights"]:
            insight = Insight(
                competitor_id=competitor.id,
                diff_id=diff.id,
                category=item["category"],
                claim=item["claim"],
                confidence=item.get("confidence"),
            )
            session.add(insight)
            session.flush()
            insight_ids.append(str(insight.id))

        set_job_status(job_id=job.id, status=JobStatus.RUNNING.value, progress=80, step="insights_saved")

        report = create_report(
            session,
            org_id=competitor.org_id,
            title=generated["report_title"],
            summary=generated["report_summary"],
        )
        session.flush()

        result = {
            "competitor_id": str(competitor.id),
            "snapshot_id": str(new_snapshot.id),
            "diff_id": str(diff.id),
            "insight_ids": insight_ids,
            "report_id": str(report.id),
            "source": generated["source"],
        }

        details = dict(job.details or {})
        details["result"] = result
        details["error"] = None
        job.details = details
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.now(timezone.utc)
        session.commit()

        invalidate_insights_cache(competitor.id)
        set_job_status(
            job_id=job.id,
            status=JobStatus.COMPLETED.value,
            progress=100,
            step="completed",
            extra={"report_id": report.id},
        )
        return result
    except Exception as exc:
        logger.exception("Analysis pipeline failed for job %s", job_id)
        _mark_job_failed(parsed_job_id, exc)
        raise
    finally:
        session.close()


def _get_job_or_raise(session, job_id: UUID) -> Job:
    job = get_job_by_id(session, job_id=job_id)
    if job is None:
        raise ValueError(f"Job {job_id} was not found.")
    return job


def _mark_job_failed(job_id: UUID, exc: Exception) -> None:
    session = SessionLocal()
    try:
        job = get_job_by_id(session, job_id=job_id)
        if job is None:
            return

        details = dict(job.details or {})
        details["error"] = {"type": exc.__class__.__name__, "message": str(exc)}
        job.details = details
        job.status = JobStatus.FAILED
        job.completed_at = datetime.now(timezone.utc)
        session.commit()

        set_job_status(
            job_id=job.id,
            status=JobStatus.FAILED.value,
            progress=100,
            step="failed",
            extra={"error": str(exc)},
        )
    finally:
        session.close()


def _build_snapshot_content(*, competitor_name: str, competitor_domain: str, prompt: str | None) -> str:
    prompt_fragment = f" Prompt focus: {prompt}." if prompt else ""
    now = datetime.now(timezone.utc).isoformat()
    return (
        f"{competitor_name} ({competitor_domain}) site capture at {now}."
        " Pricing page mentions faster onboarding, improved analytics, and enterprise support tiers."
        f"{prompt_fragment}"
    )


def _build_diff_text(previous_content: str | None, current_content: str) -> str:
    if not previous_content:
        return "Initial capture created for competitor. New capabilities and pricing language detected."

    return (
        "Detected changes between previous and current snapshot: updated positioning, refreshed analytics "
        "messaging, and stronger enterprise support claims."
    )


def _generate_analysis_bundle(
    *,
    competitor_name: str,
    competitor_domain: str,
    request_payload: dict[str, Any],
    diff_text: str,
) -> dict[str, Any]:
    payload = {
        "competitor_name": competitor_name,
        "competitor_domain": competitor_domain,
        "diff_text": diff_text,
        **request_payload,
    }

    try:
        agent_payload = request_agent_analysis(payload)
        return {
            "source": "ai-agent",
            "report_title": agent_payload.get("report_title") or f"{competitor_name} Analysis Report",
            "report_summary": agent_payload.get("report_summary")
            or f"AI-generated summary for {competitor_name} based on the latest website changes.",
            "insights": _normalize_insights(agent_payload.get("insights")),
        }
    except AIAgentIntegrationError:
        logger.info("AI agent unavailable or disabled. Falling back to mock analysis for %s.", competitor_name)

    return {
        "source": "mock",
        "report_title": f"{competitor_name} Competitive Update",
        "report_summary": (
            f"{competitor_name} introduced stronger analytics messaging and clearer enterprise value on "
            f"{competitor_domain}. The latest diff suggests a sharper enterprise sales motion."
        ),
        "insights": [
            {
                "category": "positioning",
                "claim": f"{competitor_name} is emphasizing faster onboarding in new page copy.",
                "confidence": 0.87,
            },
            {
                "category": "product",
                "claim": f"{competitor_name} is highlighting expanded analytics capabilities.",
                "confidence": 0.82,
            },
            {
                "category": "sales",
                "claim": "Enterprise support and tier-based messaging appear more prominent than before.",
                "confidence": 0.79,
            },
        ],
    }


def _normalize_insights(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []

    normalized: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        confidence = item.get("confidence")
        normalized.append(
            {
                "category": str(item.get("category", "general")),
                "claim": str(item.get("claim", "No claim provided.")),
                "confidence": float(confidence) if confidence is not None else None,
            }
        )
    return normalized
