from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.crud.organization import get_accessible_org_ids
from app.db.models import Competitor, Job, Report, User
from app.utils.exceptions import BadRequestError, ForbiddenError, NotFoundError


def get_user_org_ids(db: Session, *, user: User) -> list[UUID]:
    org_ids = get_accessible_org_ids(db, user_id=user.id)
    if not org_ids:
        raise ForbiddenError("The authenticated user is not assigned to any organization.")
    return org_ids


def resolve_target_org_id(db: Session, *, user: User, requested_org_id: UUID | None = None) -> UUID:
    org_ids = get_user_org_ids(db, user=user)
    if requested_org_id is not None:
        if requested_org_id not in org_ids:
            raise ForbiddenError("You do not have access to the requested organization.")
        return requested_org_id
    if len(org_ids) == 1:
        return org_ids[0]
    raise BadRequestError("Multiple organizations found. Please provide an org_id explicitly.")


def ensure_competitor_access(db: Session, *, user: User, competitor: Competitor | None) -> Competitor:
    if competitor is None:
        raise NotFoundError("Competitor not found.")
    if competitor.org_id not in get_user_org_ids(db, user=user):
        raise ForbiddenError("You do not have access to this competitor.")
    return competitor


def ensure_job_access(db: Session, *, user: User, job: Job | None) -> Job:
    if job is None:
        raise NotFoundError("Job not found.")
    if job.org_id is None or job.org_id not in get_user_org_ids(db, user=user):
        raise ForbiddenError("You do not have access to this job.")
    return job


def ensure_report_access(db: Session, *, user: User, report: Report | None) -> Report:
    if report is None:
        raise NotFoundError("Report not found.")
    if report.org_id not in get_user_org_ids(db, user=user):
        raise ForbiddenError("You do not have access to this report.")
    return report
