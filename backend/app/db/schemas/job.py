from __future__ import annotations

from uuid import UUID

from app.db.schemas.common import TimestampedModel


class JobRead(TimestampedModel):
    org_id: UUID | None
    status: str
    progress: int
    step: str | None
    error: str | None
    details: dict
