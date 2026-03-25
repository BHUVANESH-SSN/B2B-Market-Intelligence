from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.enums import JobStatus
from app.db.models.mixins import UUIDPrimaryKeyMixin
from app.db.session import Base


class Job(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "jobs"
    __table_args__ = (Index("idx_jobs_status", "status"),)

    org_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name="job_status", native_enum=False),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    details: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="jobs")
