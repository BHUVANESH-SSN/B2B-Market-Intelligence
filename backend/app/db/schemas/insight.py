from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class InsightRead(BaseModel):
    id: UUID
    competitor_id: UUID
    diff_id: UUID
    category: str
    claim: str
    confidence: float | None = None
    created_at: datetime
