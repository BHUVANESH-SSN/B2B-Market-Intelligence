from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.db.schemas.insight import InsightRead
from app.services.insight_service import list_insights_for_user

router = APIRouter()


@router.get("", response_model=list[InsightRead])
def list_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[InsightRead]:
    return list_insights_for_user(db, user=current_user)


@router.get("/{competitor_id}", response_model=list[InsightRead])
def list_competitor_insights(
    competitor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[InsightRead]:
    return list_insights_for_user(db, user=current_user, competitor_id=competitor_id)
