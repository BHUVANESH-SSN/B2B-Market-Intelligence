from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganizationMembershipRead(BaseModel):
    org_id: UUID
    org_name: str
    role: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    clerk_user_id: str | None
    name: str
    email: str
    is_active: bool
    created_at: datetime


class CurrentUserResponse(UserRead):
    organizations: list[OrganizationMembershipRead]
    session_id: str | None = None
    token_claims: dict[str, Any] | None = None
