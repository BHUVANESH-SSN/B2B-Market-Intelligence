from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.competitor import Competitor


def create_competitor(db: Session, *, org_id: UUID, name: str, domain: str) -> Competitor:
    competitor = Competitor(org_id=org_id, name=name, domain=domain)
    db.add(competitor)
    db.flush()
    return competitor


def get_competitor(db: Session, *, competitor_id: UUID, org_id: UUID) -> Competitor | None:
    return db.scalar(
        select(Competitor).where(Competitor.id == competitor_id, Competitor.org_id == org_id)
    )


def list_competitors(db: Session, *, org_id: UUID) -> list[Competitor]:
    return list(
        db.scalars(select(Competitor).where(Competitor.org_id == org_id).order_by(Competitor.created_at.desc()))
    )


def delete_competitor(db: Session, *, competitor_id: UUID, org_id: UUID) -> bool:
    result = db.execute(
        delete(Competitor).where(Competitor.id == competitor_id, Competitor.org_id == org_id)
    )
    return result.rowcount > 0
