from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.db.models.enums import JobStatus


class JobRead(BaseModel):
    id: UUID
    status: JobStatus
    progress: int = 0
    step: str = "pending"
    started_at: datetime
    completed_at: datetime | None = None
    details: dict[str, Any] | None = None
