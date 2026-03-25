from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.crud.job import get_job_by_id
from app.db.models import User
from app.db.models.enums import JobStatus
from app.db.schemas.job import JobRead
from app.services.access_control import ensure_job_access
from app.services.redis_state import get_job_status


def get_job_for_user(db: Session, *, user: User, job_id: UUID) -> JobRead:
    job = ensure_job_access(db, user=user, job=get_job_by_id(db, job_id=job_id))
    redis_state = get_job_status(job.id)
    progress = int(redis_state.get("progress", 0))
    step = redis_state.get("step", job.status.value)
    status_value = redis_state.get("status", job.status.value)

    return JobRead(
        id=job.id,
        status=JobStatus(status_value),
        progress=progress,
        step=step,
        started_at=job.started_at,
        completed_at=job.completed_at,
        details=job.details,
    )
