from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.crud.job import create_job, get_job
from app.db.models.enums import JobStatus
from app.db.models.user import User
from app.db.schemas.analysis import AnalysisRunRequest
from app.services.competitor_service import get_competitor_for_user
from app.services.redis_state import get_job_status, set_job_status
from app.services.user_context import get_primary_membership
from app.workers.tasks import run_market_analysis


def enqueue_analysis(db: Session, *, user: User, payload: AnalysisRunRequest):
    membership = get_primary_membership(db, user)
    competitor = get_competitor_for_user(db, user=user, competitor_id=payload.competitor_id)

    details = {
        "competitor": {
            "id": str(competitor.id),
            "name": competitor.name,
            "domain": competitor.domain,
        },
        "url": str(payload.url) if payload.url else f"https://{competitor.domain}",
        "current_html": payload.current_html,
        "previous_html": payload.previous_html,
        "history_claims": payload.history_claims,
    }
    job = create_job(
        db,
        org_id=membership.org_id,
        status=JobStatus.QUEUED.value,
        progress=0,
        step="queued",
        details=details,
    )
    db.commit()
    db.refresh(job)

    set_job_status(str(job.id), status=job.status, progress=job.progress, step=job.step or "queued")
    run_market_analysis.delay(str(job.id))
    return job


def get_job_for_user(db: Session, *, user: User, job_id):
    membership = get_primary_membership(db, user)
    job = get_job(db, job_id=job_id)
    if job is None or job.org_id != membership.org_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    redis_status = get_job_status(str(job.id))
    if redis_status:
        job.details = {**job.details, "redis_status": redis_status}
    return job
