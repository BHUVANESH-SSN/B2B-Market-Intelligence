from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ClerkPrincipal
from app.db.crud.membership import create_membership
from app.db.crud.user import (
    create_default_organization,
    create_user,
    get_user_by_clerk_user_id,
    get_user_by_email,
)
from app.db.models.enums import MembershipRole
from app.db.models.user import User


def _extract_email(payload: dict[str, Any]) -> str:
    primary_email_id = payload.get("primary_email_address_id")
    for item in payload.get("email_addresses", []):
        if item.get("id") == primary_email_id and item.get("email_address"):
            return str(item["email_address"]).strip().lower()
    for item in payload.get("email_addresses", []):
        if item.get("email_address"):
            return str(item["email_address"]).strip().lower()
    email = str(payload.get("email_address", "")).strip().lower()
    return email


def _extract_name(payload: dict[str, Any], principal: ClerkPrincipal) -> str:
    full_name = str(payload.get("full_name", "")).strip()
    if full_name:
        return full_name
    first_name = str(payload.get("first_name", "")).strip()
    last_name = str(payload.get("last_name", "")).strip()
    combined = " ".join(part for part in (first_name, last_name) if part).strip()
    if combined:
        return combined
    token_name = str(principal.claims.get("name", "")).strip()
    if token_name:
        return token_name
    return principal.clerk_user_id


def _fetch_clerk_user(principal: ClerkPrincipal) -> dict[str, Any]:
    if not settings.clerk_secret_key:
        claims = principal.claims
        email = str(claims.get("email", "")).strip().lower()
        name = str(claims.get("name", "")).strip() or principal.clerk_user_id
        if not email:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Clerk secret key is not configured, and token claims do not include email.",
            )
        return {"email_addresses": [{"email_address": email}], "full_name": name}

    url = f"{settings.clerk_api_url.rstrip('/')}/users/{principal.clerk_user_id}"
    headers = {"Authorization": settings.clerk_secret_key}
    try:
        response = httpx.get(url, headers=headers, timeout=15.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to fetch Clerk user details.",
        ) from exc
    return response.json()


def get_or_sync_user_from_clerk(db: Session, principal: ClerkPrincipal) -> User:
    existing_user = get_user_by_clerk_user_id(db, principal.clerk_user_id)
    if existing_user is not None:
        return existing_user

    payload = _fetch_clerk_user(principal)
    email = _extract_email(payload)
    name = _extract_name(payload, principal)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to determine user email from Clerk.",
        )

    existing_email_user = get_user_by_email(db, email)
    if existing_email_user is not None:
        existing_email_user.clerk_user_id = principal.clerk_user_id
        db.add(existing_email_user)
        db.commit()
        db.refresh(existing_email_user)
        return existing_email_user

    user = create_user(db, name=name, email=email, clerk_user_id=principal.clerk_user_id)
    organization = create_default_organization(db, name=f"{name}'s Workspace")
    create_membership(db, user_id=user.id, org_id=organization.id, role=MembershipRole.OWNER)
    db.commit()
    db.refresh(user)
    return user
