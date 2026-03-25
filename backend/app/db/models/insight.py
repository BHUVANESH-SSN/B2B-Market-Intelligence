from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.competitor import Competitor
    from app.db.models.diff import Diff


class Insight(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "insights"
    __table_args__ = (
        Index("idx_insights_competitor", "competitor_id"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_insights_confidence_range"),
    )

    competitor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    diff_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("diffs.id", ondelete="CASCADE"),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    source_section: Mapped[str | None] = mapped_column(String(100), nullable=True)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    scores: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    competitor: Mapped["Competitor"] = relationship(back_populates="insights")
    diff: Mapped["Diff"] = relationship(back_populates="insights")
