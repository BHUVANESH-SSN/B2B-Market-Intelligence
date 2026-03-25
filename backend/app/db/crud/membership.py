from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.enums import MembershipRole
from app.db.models.membership import Membership


def create_membership(
    db: Session,
    *,
    user_id,
    org_id,
    role: MembershipRole = MembershipRole.MEMBER,
) -> Membership:
    membership = Membership(user_id=user_id, org_id=org_id, role=role)
    db.add(membership)
    db.flush()
    return membership
