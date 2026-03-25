from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.job import Job


def create_job(
    db: Session,
    *,
    org_id,
    status: str,
    progress: int,
    step: str | None,
    details: dict,
) -> Job:
    job = Job(org_id=org_id, status=status, progress=progress, step=step, details=details)
    db.add(job)
    db.flush()
    return job


def get_job(db: Session, *, job_id) -> Job | None:
    return db.scalar(select(Job).where(Job.id == job_id))
