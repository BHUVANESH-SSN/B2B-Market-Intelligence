from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Competitor, Insight


def list_insights_by_org_ids(db: Session, *, org_ids: list[UUID]) -> list[Insight]:
    stmt = (
        select(Insight)
        .join(Competitor, Competitor.id == Insight.competitor_id)
        .where(Competitor.org_id.in_(org_ids))
        .order_by(Insight.created_at.desc())
    )
    return list(db.scalars(stmt))


def list_insights_by_competitor(db: Session, *, competitor_id: UUID) -> list[Insight]:
    stmt = select(Insight).where(Insight.competitor_id == competitor_id).order_by(Insight.created_at.desc())
    return list(db.scalars(stmt))
