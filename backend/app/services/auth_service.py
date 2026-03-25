from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.db.models import User
from app.db.schemas.auth import CurrentUserResponse
from app.services.clerk_service import build_current_user_response


def get_current_user_response(db: Session, user: User, claims: dict[str, Any]) -> CurrentUserResponse:
    return build_current_user_response(db, user, claims)
