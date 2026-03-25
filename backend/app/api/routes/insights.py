from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.schemas.insight import InsightRead
from app.db.session import get_db
from app.services.insight_service import get_insights, get_insights_for_competitor


router = APIRouter()


@router.get("", response_model=list[InsightRead])
async def list_insights(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[InsightRead]:
    return get_insights(db, user=user)


@router.get("/{competitor_id}", response_model=list[InsightRead])
async def list_competitor_insights(
    competitor_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[InsightRead]:
    return get_insights_for_competitor(db, user=user, competitor_id=competitor_id)
