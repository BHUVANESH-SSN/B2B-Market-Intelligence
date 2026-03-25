from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import PASSWORD_PLACEHOLDER
from app.db.models.organization import Organization
from app.db.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_user_by_clerk_user_id(db: Session, clerk_user_id: str) -> User | None:
    return db.scalar(select(User).where(User.clerk_user_id == clerk_user_id))


def create_user(
    db: Session,
    *,
    name: str,
    email: str,
    clerk_user_id: str | None = None,
) -> User:
    user = User(
        name=name,
        email=email,
        clerk_user_id=clerk_user_id,
        password_hash=PASSWORD_PLACEHOLDER,
    )
    db.add(user)
    db.flush()
    return user


def create_default_organization(db: Session, *, name: str) -> Organization:
    organization = Organization(name=name)
    db.add(organization)
    db.flush()
    return organization
