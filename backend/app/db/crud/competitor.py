from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Competitor


def create_competitor(db: Session, *, org_id: UUID, name: str, domain: str) -> Competitor:
    competitor = Competitor(org_id=org_id, name=name, domain=domain.lower())
    db.add(competitor)
    db.flush()
    return competitor


def list_competitors_by_org_ids(db: Session, *, org_ids: list[UUID]) -> list[Competitor]:
    stmt = select(Competitor).where(Competitor.org_id.in_(org_ids)).order_by(Competitor.created_at.desc())
    return list(db.scalars(stmt))


def get_competitor_by_id(db: Session, *, competitor_id: UUID) -> Competitor | None:
    return db.get(Competitor, competitor_id)


def get_competitor_by_domain(db: Session, *, org_id: UUID, domain: str) -> Competitor | None:
    stmt = select(Competitor).where(Competitor.org_id == org_id, Competitor.domain == domain.lower())
    return db.scalar(stmt)


def delete_competitor(db: Session, *, competitor: Competitor) -> None:
    db.delete(competitor)
