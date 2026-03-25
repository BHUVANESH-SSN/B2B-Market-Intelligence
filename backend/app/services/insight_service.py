from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.crud.insight import list_insights_for_competitor, list_insights_for_org
from app.db.models.user import User
from app.services.redis_state import get_cached_competitor_insights
from app.services.user_context import get_primary_membership


def get_insights(db: Session, *, user: User):
    membership = get_primary_membership(db, user)
    return list_insights_for_org(db, org_id=membership.org_id)


def get_insights_for_competitor(db: Session, *, user: User, competitor_id):
    cached = get_cached_competitor_insights(str(competitor_id))
    if cached is not None:
        return cached

    membership = get_primary_membership(db, user)
    return list_insights_for_competitor(db, org_id=membership.org_id, competitor_id=competitor_id)
