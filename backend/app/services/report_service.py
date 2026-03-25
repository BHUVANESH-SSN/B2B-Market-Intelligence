from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.crud.report import get_report_by_id
from app.db.models import User
from app.db.schemas.report import ReportRead
from app.services.access_control import ensure_report_access


def get_report_for_user(db: Session, *, user: User, report_id: UUID) -> ReportRead:
    report = ensure_report_access(db, user=user, report=get_report_by_id(db, report_id=report_id))
    return ReportRead(
        id=report.id,
        org_id=report.org_id,
        title=report.title,
        summary=report.summary,
        created_at=report.created_at,
    )
