from __future__ import annotations

from sqlalchemy import join, select
from sqlalchemy.orm import Session

from app.db.models.competitor import Competitor
from app.db.models.insight import Insight


def create_insight(
    db: Session,
    *,
    competitor_id,
    diff_id,
    category: str,
    claim: str,
    confidence: float,
    source_section: str | None,
    evidence: str | None,
    scores: dict,
) -> Insight:
    insight = Insight(
        competitor_id=competitor_id,
        diff_id=diff_id,
        category=category,
        claim=claim,
        confidence=confidence,
        source_section=source_section,
        evidence=evidence,
        scores=scores,
    )
    db.add(insight)
    db.flush()
    return insight


def list_insights_for_org(db: Session, *, org_id) -> list[Insight]:
    statement = (
        select(Insight)
        .select_from(join(Insight, Competitor, Insight.competitor_id == Competitor.id))
        .where(Competitor.org_id == org_id)
        .order_by(Insight.created_at.desc())
    )
    return list(db.scalars(statement))


def list_insights_for_competitor(db: Session, *, org_id, competitor_id) -> list[Insight]:
    statement = (
        select(Insight)
        .select_from(join(Insight, Competitor, Insight.competitor_id == Competitor.id))
        .where(Competitor.org_id == org_id, Competitor.id == competitor_id)
        .order_by(Insight.created_at.desc())
    )
    return list(db.scalars(statement))
