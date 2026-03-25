from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.db.models.membership import Membership
from app.db.models.user import User


def get_primary_membership(db: Session, user: User) -> Membership:
    statement = (
        select(Membership)
        .options(selectinload(Membership.organization))
        .where(Membership.user_id == user.id)
        .order_by(Membership.role.asc())
    )
    membership = db.scalar(statement)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not attached to any organization.",
        )
    return membership
