from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.crud.competitor import get_competitor_by_id
from app.db.crud.job import create_job
from app.db.models import User
from app.db.models.enums import JobStatus
from app.db.schemas.analysis import AnalysisRunRequest, AnalysisRunResponse
from app.services.access_control import ensure_competitor_access, resolve_target_org_id
from app.services.redis_state import set_job_status
from app.workers.celery_app import celery_app


def queue_analysis_job(db: Session, *, user: User, payload: AnalysisRunRequest) -> AnalysisRunResponse:
    competitor = ensure_competitor_access(
        db,
        user=user,
        competitor=get_competitor_by_id(db, competitor_id=payload.competitor_id),
    )
    org_id = resolve_target_org_id(db, user=user, requested_org_id=payload.org_id or competitor.org_id)

    job = create_job(
        db,
        org_id=org_id,
        status=JobStatus.QUEUED,
        details={
            "request": payload.model_dump(mode="json"),
            "result": None,
            "error": None,
        },
    )
    db.commit()
    db.refresh(job)

    set_job_status(job_id=job.id, status=JobStatus.QUEUED.value, progress=0, step="queued")
    task = celery_app.send_task("analysis.run_market_analysis", args=[str(job.id)])

    details = dict(job.details or {})
    details["celery_task_id"] = task.id
    job.details = details
    db.commit()

    return AnalysisRunResponse(job_id=job.id)
