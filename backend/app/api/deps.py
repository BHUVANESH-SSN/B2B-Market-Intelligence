from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import verify_clerk_session_token
from app.db.models import User
from app.db.session import SessionLocal
from app.services.clerk_service import get_or_sync_user_from_clerk_claims
from app.utils.exceptions import UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthContext:
    user: User
    claims: dict[str, Any]


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_context(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    if credentials is None:
        raise UnauthorizedError("Authentication credentials were not provided.")

    try:
        claims = verify_clerk_session_token(credentials.credentials)
    except ValueError as exc:
        raise UnauthorizedError(str(exc)) from exc

    user = get_or_sync_user_from_clerk_claims(db, claims)
    if user is None:
        raise UnauthorizedError("Authenticated Clerk user was not found.")
    return AuthContext(user=user, claims=claims)


def get_current_user(auth_context: AuthContext = Depends(get_auth_context)) -> User:
    return auth_context.user
