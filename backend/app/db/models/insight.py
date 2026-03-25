from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, Float, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class Insight(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "insights"
    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_insights_confidence_range"),
        Index("idx_insights_competitor", "competitor_id"),
    )

    competitor_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    diff_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("diffs.id", ondelete="CASCADE"),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(Text, nullable=False)
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    competitor: Mapped["Competitor"] = relationship("Competitor", back_populates="insights")
    diff: Mapped["Diff"] = relationship("Diff", back_populates="insights")
