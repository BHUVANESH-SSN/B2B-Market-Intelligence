from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AnalysisRunRequest(BaseModel):
    competitor_id: UUID
    org_id: UUID | None = None
    prompt: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class AnalysisRunResponse(BaseModel):
    job_id: UUID
