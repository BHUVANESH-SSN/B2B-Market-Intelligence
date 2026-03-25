from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.competitor import Competitor
    from app.db.models.insight import Insight
    from app.db.models.snapshot import Snapshot


class Diff(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "diffs"
    __table_args__ = (Index("idx_diffs_competitor", "competitor_id"),)

    competitor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    old_snapshot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("snapshots.id", ondelete="SET NULL"),
        nullable=True,
    )
    new_snapshot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("snapshots.id", ondelete="SET NULL"),
        nullable=True,
    )
    diff_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    diff_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    competitor: Mapped["Competitor"] = relationship(back_populates="diffs")
    old_snapshot: Mapped["Snapshot | None"] = relationship(
        back_populates="old_diffs",
        foreign_keys=[old_snapshot_id],
    )
    new_snapshot: Mapped["Snapshot | None"] = relationship(
        back_populates="new_diffs",
        foreign_keys=[new_snapshot_id],
    )
    insights: Mapped[list["Insight"]] = relationship(
        back_populates="diff",
        cascade="all, delete-orphan",
    )
