from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.crud.diff import create_diff
from app.db.crud.insight import create_insight
from app.db.crud.job import get_job
from app.db.crud.report import create_report
from app.db.crud.snapshot import create_snapshot, get_latest_snapshot
from app.db.models.enums import JobStatus
from app.services.ai_agent_service import run_ai_pipeline
from app.services.redis_state import cache_competitor_insights, set_job_status
from app.services.scraper_service import run_scraper_pipeline


def _build_report_summary(competitor_name: str, insights: list[dict], recommendations: list[dict]) -> str:
    top_claims = [item.get("claim", "").strip() for item in insights[:3] if item.get("claim")]
    top_actions = [item.get("title", "").strip() for item in recommendations[:2] if item.get("title")]
    sentences = []
    if top_claims:
        sentences.append(f"Key changes detected for {competitor_name}: " + "; ".join(top_claims) + ".")
    if top_actions:
        sentences.append("Recommended actions: " + "; ".join(top_actions) + ".")
    return " ".join(sentences) or f"No major changes were detected for {competitor_name}."


def process_analysis_job(db: Session, job_id: str) -> dict[str, str]:
    job = get_job(db, job_id=job_id)
    if job is None:
        raise ValueError(f"Job not found: {job_id}")

    details = dict(job.details or {})
    competitor = job.details["competitor"]
    org_id = job.org_id
    competitor_id = competitor["id"]

    job.status = JobStatus.RUNNING.value
    job.progress = 10
    job.step = "scraping"
    db.add(job)
    db.commit()
    set_job_status(job_id, status=job.status, progress=job.progress, step=job.step)

    previous_snapshot = get_latest_snapshot(db, competitor_id=competitor_id)
    scraper_result = run_scraper_pipeline(
        competitor_name=competitor["name"],
        url=details.get("url"),
        current_html=details.get("current_html"),
        previous_html=details.get("previous_html") or (previous_snapshot.content if previous_snapshot else None),
    )

    new_snapshot = create_snapshot(
        db,
        competitor_id=competitor_id,
        content=scraper_result.current_html,
        content_hash=scraper_result.content_hash,
        storage_path=scraper_result.snapshot_path,
    )
    diff = create_diff(
        db,
        competitor_id=competitor_id,
        old_snapshot_id=previous_snapshot.id if previous_snapshot else None,
        new_snapshot_id=new_snapshot.id,
        diff_payload=scraper_result.diffs,
    )
    db.commit()

    job.status = JobStatus.RUNNING.value
    job.progress = 55
    job.step = "analysis"
    db.add(job)
    db.commit()
    set_job_status(job_id, status=job.status, progress=job.progress, step=job.step)

    ai_input = {
        "competitor": competitor["name"],
        "diffs": scraper_result.diffs,
        "history_claims": details.get("history_claims", []),
    }
    ai_result = run_ai_pipeline(ai_input)

    created_insights = []
    for item in ai_result.insights:
        insight = create_insight(
            db,
            competitor_id=competitor_id,
            diff_id=diff.id,
            category=str(item.get("category", "other")),
            claim=str(item.get("claim", "")),
            confidence=float(item.get("confidence", 0.0)),
            source_section=item.get("source_section"),
            evidence=item.get("evidence"),
            scores={
                "novelty_score": item.get("novelty_score", 0.0),
                "frequency_score": item.get("frequency_score", 0.0),
                "recency_score": item.get("recency_score", 0.0),
                "priority_score": item.get("priority_score", 0.0),
            },
        )
        created_insights.append(insight)

    report = create_report(
        db,
        org_id=org_id,
        competitor_id=competitor_id,
        job_id=job.id,
        title=f"{competitor['name']} analysis report",
        summary=_build_report_summary(competitor["name"], ai_result.insights, ai_result.recommendations),
        recommendations=ai_result.recommendations,
        metadata={
            **ai_result.metadata,
            "diffs": scraper_result.diffs,
            "sections": scraper_result.current_sections,
            "snapshot_path": scraper_result.snapshot_path,
            "diff_id": str(diff.id),
        },
    )
    db.commit()

    job.status = JobStatus.COMPLETED.value
    job.progress = 100
    job.step = "completed"
    job.details = {
        **details,
        "result": {
            "report_id": str(report.id),
            "diff_id": str(diff.id),
            "insight_count": len(created_insights),
        },
    }
    db.add(job)
    db.commit()
    db.refresh(job)

    cache_competitor_insights(
        str(competitor_id),
        [
            {
                "id": str(item.id),
                "created_at": item.created_at.isoformat(),
                "competitor_id": str(item.competitor_id),
                "diff_id": str(item.diff_id),
                "claim": item.claim,
                "category": item.category,
                "confidence": item.confidence,
                "source_section": item.source_section,
                "evidence": item.evidence,
                "scores": item.scores,
            }
            for item in created_insights
        ],
    )
    set_job_status(
        job_id,
        status=job.status,
        progress=job.progress,
        step=job.step,
        extra=job.details.get("result"),
    )
    return {"report_id": str(report.id)}
