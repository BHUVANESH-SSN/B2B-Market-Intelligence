from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.crud.organization import add_user_to_organization, create_organization, get_accessible_orgs
from app.db.crud.user import create_user, get_user_by_clerk_user_id, get_user_by_email
from app.db.models import User
from app.db.models.enums import OrganizationRole
from app.db.schemas.auth import CurrentUserResponse
from app.utils.exceptions import ConflictError, UnauthorizedError


def get_or_sync_user_from_clerk_claims(db: Session, claims: dict[str, Any]) -> User:
    clerk_user_id = claims.get("sub")
    if not clerk_user_id:
        raise UnauthorizedError("Clerk token subject is missing.")

    user = get_user_by_clerk_user_id(db, clerk_user_id)
    if user is not None:
        return user

    profile = fetch_clerk_user_profile(clerk_user_id)
    email = extract_primary_email(profile)
    name = extract_display_name(profile)

    existing = get_user_by_email(db, email)
    try:
        if existing is not None:
            if existing.clerk_user_id and existing.clerk_user_id != clerk_user_id:
                raise ConflictError("This email is already linked to a different Clerk account.")
            existing.clerk_user_id = clerk_user_id
            existing.name = name
            if existing.password_hash == "":
                existing.password_hash = "clerk_managed_auth"
            db.commit()
            db.refresh(existing)
            return existing

        user = create_user(
            db,
            name=name,
            email=email,
            password_hash="clerk_managed_auth",
            clerk_user_id=clerk_user_id,
        )
        organization = create_organization(db, name=f"{name}'s Workspace")
        add_user_to_organization(
            db,
            user_id=user.id,
            org_id=organization.id,
            role=OrganizationRole.OWNER,
        )
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def build_current_user_response(db: Session, user: User, claims: dict[str, Any]) -> CurrentUserResponse:
    memberships = get_accessible_orgs(db, user_id=user.id)
    return CurrentUserResponse(
        id=user.id,
        clerk_user_id=user.clerk_user_id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        organizations=[
            {"org_id": org_id, "org_name": org_name, "role": role}
            for org_id, org_name, role in memberships
        ],
        session_id=claims.get("sid"),
        token_claims=_filtered_claims(claims),
    )


def fetch_clerk_user_profile(clerk_user_id: str) -> dict[str, Any]:
    if not settings.clerk_secret_key:
        raise UnauthorizedError("CLERK_SECRET_KEY is required to sync Clerk users into the backend.")

    url = f"{settings.clerk_api_url.rstrip('/')}/users/{clerk_user_id}"
    headers = {"Authorization": settings.clerk_secret_key}

    try:
        response = httpx.get(url, headers=headers, timeout=15.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise UnauthorizedError(f"Unable to fetch Clerk user profile: {exc}") from exc

    payload = response.json()
    if not isinstance(payload, dict):
        raise UnauthorizedError("Unexpected Clerk user profile response.")
    return payload


def extract_primary_email(profile: dict[str, Any]) -> str:
    primary_id = profile.get("primary_email_address_id")
    addresses = profile.get("email_addresses") or []
    for item in addresses:
        if item.get("id") == primary_id and item.get("email_address"):
            return str(item["email_address"]).lower()
    for item in addresses:
        if item.get("email_address"):
            return str(item["email_address"]).lower()
    raise UnauthorizedError("Clerk user profile does not contain an email address.")


def extract_display_name(profile: dict[str, Any]) -> str:
    first_name = (profile.get("first_name") or "").strip()
    last_name = (profile.get("last_name") or "").strip()
    full_name = " ".join(part for part in [first_name, last_name] if part).strip()
    if full_name:
        return full_name
    username = (profile.get("username") or "").strip()
    if username:
        return username
    return extract_primary_email(profile).split("@", 1)[0]


def _filtered_claims(claims: dict[str, Any]) -> dict[str, Any]:
    keys = ["iss", "sub", "sid", "azp", "org_id", "org_role", "org_slug"]
    return {key: claims.get(key) for key in keys if claims.get(key) is not None}
