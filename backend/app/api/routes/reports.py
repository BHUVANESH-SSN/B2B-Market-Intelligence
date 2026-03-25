from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.db.schemas.report import ReportRead
from app.services.report_service import get_report_for_user

router = APIRouter()


@router.get("/{report_id}", response_model=ReportRead)
def get_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ReportRead:
    return get_report_for_user(db, user=current_user, report_id=report_id)
