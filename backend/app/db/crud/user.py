from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email.lower())
    return db.scalar(stmt)


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, *, name: str, email: str, password_hash: str) -> User:
    user = User(name=name, email=email.lower(), password_hash=password_hash)
    db.add(user)
    db.flush()
    return user
