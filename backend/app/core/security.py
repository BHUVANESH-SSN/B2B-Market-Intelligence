from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import bcrypt
import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient

from app.core.config import settings


PASSWORD_PLACEHOLDER = "clerk_managed_auth"


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash or password_hash == PASSWORD_PLACEHOLDER:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


@dataclass(slots=True)
class ClerkPrincipal:
    clerk_user_id: str
    session_id: str | None
    claims: dict[str, Any]


def verify_clerk_session_token(token: str) -> ClerkPrincipal:
    if not settings.clerk_issuer or not settings.clerk_jwks_url_resolved:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Clerk is not configured on the backend.",
        )

    try:
        jwks_client = PyJWKClient(settings.clerk_jwks_url_resolved)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Clerk token.",
        ) from exc

    azp = str(claims.get("azp", "")).strip()
    allowed_parties = settings.clerk_authorized_parties_list
    if allowed_parties and azp and azp not in allowed_parties:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token authorized party is not allowed.",
        )

    clerk_user_id = str(claims.get("sub", "")).strip()
    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clerk token does not contain a user id.",
        )

    return ClerkPrincipal(
        clerk_user_id=clerk_user_id,
        session_id=str(claims.get("sid", "")).strip() or None,
        claims=claims,
    )
