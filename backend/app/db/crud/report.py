from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Report


def create_report(db: Session, *, org_id: UUID, title: str | None, summary: str | None) -> Report:
    report = Report(org_id=org_id, title=title, summary=summary)
    db.add(report)
    db.flush()
    return report


def get_report_by_id(db: Session, *, report_id: UUID) -> Report | None:
    return db.get(Report, report_id)
