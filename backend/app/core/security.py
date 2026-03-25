from __future__ import annotations

from functools import lru_cache
from typing import Any

import bcrypt
import jwt
from jwt import InvalidTokenError, PyJWKClient

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


@lru_cache(maxsize=4)
def _get_jwks_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url)


def verify_clerk_session_token(token: str) -> dict[str, Any]:
    if not settings.clerk_issuer:
        raise ValueError("CLERK_ISSUER is not configured.")

    jwks_url = settings.clerk_jwks_url_resolved
    if not jwks_url:
        raise ValueError("Clerk JWKS URL could not be resolved.")

    try:
        signing_key = _get_jwks_client(jwks_url).get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired Clerk session token.") from exc

    azp = claims.get("azp")
    allowed_parties = settings.clerk_authorized_parties_list
    if azp and allowed_parties and azp not in allowed_parties:
        raise ValueError("Clerk token authorized party is not allowed for this backend.")

    if not claims.get("sub"):
        raise ValueError("Clerk token is missing the subject claim.")

    return claims
