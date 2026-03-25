from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.crud.competitor import get_competitor_by_id
from app.db.crud.insight import list_insights_by_competitor, list_insights_by_org_ids
from app.db.models import Insight, User
from app.db.schemas.insight import InsightRead
from app.services.access_control import ensure_competitor_access, get_user_org_ids
from app.services.redis_state import cache_insights, get_cached_insights


def list_insights_for_user(
    db: Session,
    *,
    user: User,
    competitor_id: UUID | None = None,
) -> list[InsightRead]:
    if competitor_id is not None:
        competitor = ensure_competitor_access(
            db,
            user=user,
            competitor=get_competitor_by_id(db, competitor_id=competitor_id),
        )
        cached = get_cached_insights(competitor.id)
        if cached is not None:
            return [InsightRead(**item) for item in cached]

        insights = list_insights_by_competitor(db, competitor_id=competitor.id)
        payload = [_serialize_insight(item).model_dump(mode="json") for item in insights]
        cache_insights(competitor.id, payload)
        return [InsightRead(**item) for item in payload]

    insights = list_insights_by_org_ids(db, org_ids=get_user_org_ids(db, user=user))
    return [_serialize_insight(item) for item in insights]


def _serialize_insight(insight: Insight) -> InsightRead:
    return InsightRead(
        id=insight.id,
        competitor_id=insight.competitor_id,
        diff_id=insight.diff_id,
        category=insight.category,
        claim=insight.claim,
        confidence=insight.confidence,
        created_at=insight.created_at,
    )
