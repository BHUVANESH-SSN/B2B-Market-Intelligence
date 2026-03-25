from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.crud.report import get_report
from app.db.models.user import User
from app.services.user_context import get_primary_membership


def get_report_for_user(db: Session, *, user: User, report_id):
    membership = get_primary_membership(db, user)
    report = get_report(db, report_id=report_id, org_id=membership.org_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found.")
    return report
