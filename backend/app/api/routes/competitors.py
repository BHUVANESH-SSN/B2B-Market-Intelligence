from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.schemas.competitor import CompetitorCreate, CompetitorRead
from app.db.session import get_db
from app.services.competitor_service import (
    create_competitor_for_user,
    delete_competitor_for_user,
    list_competitors_for_user,
)


router = APIRouter()


@router.post("", response_model=CompetitorRead, status_code=status.HTTP_201_CREATED)
async def create_competitor(
    payload: CompetitorCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CompetitorRead:
    return create_competitor_for_user(db, user=user, payload=payload)


@router.get("", response_model=list[CompetitorRead])
async def list_competitors(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[CompetitorRead]:
    return list_competitors_for_user(db, user=user)


@router.delete("/{competitor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competitor(
    competitor_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    delete_competitor_for_user(db, user=user, competitor_id=competitor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
