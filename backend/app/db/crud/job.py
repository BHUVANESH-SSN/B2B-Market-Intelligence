from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Job
from app.db.models.enums import JobStatus


def create_job(
    db: Session,
    *,
    org_id: UUID,
    status: JobStatus,
    details: dict[str, Any],
) -> Job:
    job = Job(org_id=org_id, status=status, details=details)
    db.add(job)
    db.flush()
    return job


def get_job_by_id(db: Session, *, job_id: UUID) -> Job | None:
    return db.get(Job, job_id)
