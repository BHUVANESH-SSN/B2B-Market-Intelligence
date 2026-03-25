from __future__ import annotations

from sqlalchemy import join, select
from sqlalchemy.orm import Session

from app.db.models.organization import Organization
from app.db.models.report import Report


def create_report(
    db: Session,
    *,
    org_id,
    competitor_id,
    job_id,
    title: str | None,
    summary: str | None,
    recommendations: list,
    metadata: dict,
) -> Report:
    report = Report(
        org_id=org_id,
        competitor_id=competitor_id,
        job_id=job_id,
        title=title,
        summary=summary,
        recommendations=recommendations,
        report_metadata=metadata,
    )
    db.add(report)
    db.flush()
    return report


def get_report(db: Session, *, report_id, org_id) -> Report | None:
    statement = (
        select(Report)
        .select_from(join(Report, Organization, Report.org_id == Organization.id))
        .where(Report.id == report_id, Report.org_id == org_id)
    )
    return db.scalar(statement)
