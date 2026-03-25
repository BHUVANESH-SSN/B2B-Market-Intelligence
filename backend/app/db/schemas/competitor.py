from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, field_validator

from app.db.schemas.common import TimestampedModel


class CompetitorCreate(BaseModel):
    name: str
    domain: str

    @field_validator("name", "domain")
    @classmethod
    def non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value cannot be empty.")
        return cleaned


class CompetitorRead(TimestampedModel):
    org_id: UUID
    name: str
    domain: str
