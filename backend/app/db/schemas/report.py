from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReportRead(BaseModel):
    id: UUID
    org_id: UUID
    title: str | None = None
    summary: str | None = None
    created_at: datetime
