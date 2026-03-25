from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import ClerkPrincipal, verify_clerk_session_token
from app.db.models.user import User
from app.db.session import get_db
from app.services.clerk_service import get_or_sync_user_from_clerk


bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(slots=True)
class AuthContext:
    user: User
    principal: ClerkPrincipal


def get_auth_context(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer token.",
        )

    principal = verify_clerk_session_token(credentials.credentials)
    user = get_or_sync_user_from_clerk(db, principal)
    return AuthContext(user=user, principal=principal)


def get_current_user(auth: AuthContext = Depends(get_auth_context)) -> User:
    return auth.user
