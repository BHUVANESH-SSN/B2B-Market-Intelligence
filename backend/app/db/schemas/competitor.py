from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompetitorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    domain: str = Field(min_length=3, max_length=255)
    org_id: UUID | None = None


class CompetitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    org_id: UUID
    name: str
    domain: str
    created_at: datetime
