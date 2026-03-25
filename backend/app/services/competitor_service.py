from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.competitor import create_competitor, delete_competitor, get_competitor, list_competitors
from app.db.models.competitor import Competitor
from app.db.models.user import User
from app.db.schemas.competitor import CompetitorCreate
from app.services.user_context import get_primary_membership


def create_competitor_for_user(db: Session, *, user: User, payload: CompetitorCreate) -> Competitor:
    membership = get_primary_membership(db, user)
    try:
        competitor = create_competitor(
            db,
            org_id=membership.org_id,
            name=payload.name,
            domain=payload.domain.lower(),
        )
        db.commit()
        db.refresh(competitor)
        return competitor
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A competitor with that domain already exists for this organization.",
        ) from exc


def list_competitors_for_user(db: Session, *, user: User) -> list[Competitor]:
    membership = get_primary_membership(db, user)
    return list_competitors(db, org_id=membership.org_id)


def get_competitor_for_user(db: Session, *, user: User, competitor_id: UUID) -> Competitor:
    membership = get_primary_membership(db, user)
    competitor = get_competitor(db, competitor_id=competitor_id, org_id=membership.org_id)
    if competitor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competitor not found.")
    return competitor


def delete_competitor_for_user(db: Session, *, user: User, competitor_id: UUID) -> None:
    membership = get_primary_membership(db, user)
    deleted = delete_competitor(db, competitor_id=competitor_id, org_id=membership.org_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competitor not found.")
    db.commit()
