from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.crud.competitor import (
    create_competitor,
    delete_competitor,
    get_competitor_by_domain,
    get_competitor_by_id,
    list_competitors_by_org_ids,
)
from app.db.models import User
from app.db.schemas.competitor import CompetitorCreate
from app.services.access_control import ensure_competitor_access, get_user_org_ids, resolve_target_org_id
from app.utils.exceptions import ConflictError


def create_competitor_for_user(db: Session, *, user: User, payload: CompetitorCreate):
    org_id = resolve_target_org_id(db, user=user, requested_org_id=payload.org_id)
    if get_competitor_by_domain(db, org_id=org_id, domain=payload.domain) is not None:
        raise ConflictError("A competitor with this domain already exists.")

    competitor = create_competitor(db, org_id=org_id, name=payload.name, domain=payload.domain)
    db.commit()
    db.refresh(competitor)
    return competitor


def list_competitors_for_user(db: Session, *, user: User) -> list:
    return list_competitors_by_org_ids(db, org_ids=get_user_org_ids(db, user=user))


def delete_competitor_for_user(db: Session, *, user: User, competitor_id: UUID) -> None:
    competitor = ensure_competitor_access(
        db,
        user=user,
        competitor=get_competitor_by_id(db, competitor_id=competitor_id),
    )
    delete_competitor(db, competitor=competitor)
    db.commit()
