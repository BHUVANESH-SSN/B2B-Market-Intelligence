from collections.abc import Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.crud.user import get_user_by_id
from app.db.models import User
from app.db.session import SessionLocal
from app.utils.exceptions import UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise UnauthorizedError("Authentication credentials were not provided.")

    try:
        token_payload = decode_access_token(credentials.credentials)
        subject = token_payload.get("sub")
        user_id = UUID(subject) if subject else None
    except (ValueError, TypeError) as exc:
        raise UnauthorizedError("Invalid authentication token.") from exc

    if not subject:
        raise UnauthorizedError("Authentication token subject is missing.")

    user = get_user_by_id(db, user_id)
    if user is None:
        raise UnauthorizedError("Authenticated user was not found.")
    return user
