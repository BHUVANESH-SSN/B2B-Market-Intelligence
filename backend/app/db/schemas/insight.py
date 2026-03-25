from __future__ import annotations

from uuid import UUID

from app.db.schemas.common import TimestampedModel


class InsightRead(TimestampedModel):
    competitor_id: UUID
    diff_id: UUID
    category: str
    claim: str
    confidence: float
    source_section: str | None
    evidence: str | None
    scores: dict
