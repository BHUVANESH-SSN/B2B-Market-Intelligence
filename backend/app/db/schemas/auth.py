from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    organization_name: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    email: str
    password: str


class OrganizationMembershipRead(BaseModel):
    org_id: UUID
    org_name: str
    role: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime


class CurrentUserResponse(UserRead):
    organizations: list[OrganizationMembershipRead]


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: CurrentUserResponse
