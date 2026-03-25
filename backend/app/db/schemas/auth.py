from __future__ import annotations

from typing import Any
from uuid import UUID

from app.db.schemas.common import ORMModel, TimestampedModel


class OrganizationMembershipRead(ORMModel):
    id: UUID
    name: str
    role: str


class CurrentUserResponse(TimestampedModel):
    clerk_user_id: str | None
    name: str
    email: str
    is_active: bool
    organizations: list[OrganizationMembershipRead]
    session_id: str | None
    token_claims: dict[str, Any]
