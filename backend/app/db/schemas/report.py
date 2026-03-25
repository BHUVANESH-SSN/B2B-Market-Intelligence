from __future__ import annotations

from uuid import UUID

from pydantic import Field

from app.db.schemas.common import TimestampedModel


class ReportRead(TimestampedModel):
    org_id: UUID
    competitor_id: UUID | None
    job_id: UUID | None
    title: str | None
    summary: str | None
    recommendations: list
    metadata: dict = Field(validation_alias="report_metadata")
