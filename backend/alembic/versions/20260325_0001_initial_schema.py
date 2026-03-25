"""initial schema

Revision ID: 20260325_0001
Revises:
Create Date: 2026-03-25 10:55:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260325_0001"
down_revision = None
branch_labels = None
depends_on = None


membership_role = sa.Enum("OWNER", "MEMBER", name="membership_role")


def upgrade() -> None:
    membership_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)

    op.create_table(
        "organizations",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "jobs",
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=50), server_default="queued", nullable=False),
        sa.Column("progress", sa.Integer(), server_default="0", nullable=False),
        sa.Column("step", sa.String(length=120), nullable=True),
        sa.Column("error", sa.String(length=500), nullable=True),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_jobs_status", "jobs", ["status"], unique=False)

    op.create_table(
        "user_organizations",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", membership_role, server_default="MEMBER", nullable=False),
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "org_id"),
    )

    op.create_table(
        "competitors",
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("org_id", "domain", name="uq_competitors_org_domain"),
    )
    op.create_index("idx_competitors_org", "competitors", ["org_id"], unique=False)

    op.create_table(
        "snapshots",
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("storage_path", sa.Text(), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["competitor_id"], ["competitors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_snapshots_competitor", "snapshots", ["competitor_id"], unique=False)

    op.create_table(
        "diffs",
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("old_snapshot_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("new_snapshot_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("diff_text", sa.Text(), nullable=False),
        sa.Column("diff_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["competitor_id"], ["competitors.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["new_snapshot_id"], ["snapshots.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["old_snapshot_id"], ["snapshots.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_diffs_competitor", "diffs", ["competitor_id"], unique=False)

    op.create_table(
        "insights",
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("diff_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("source_section", sa.String(length=100), nullable=True),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("scores", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_insights_confidence_range"),
        sa.ForeignKeyConstraint(["competitor_id"], ["competitors.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["diff_id"], ["diffs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_insights_competitor", "insights", ["competitor_id"], unique=False)

    op.create_table(
        "reports",
        sa.Column("org_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("recommendations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["competitor_id"], ["competitors.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["org_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_index("idx_insights_competitor", table_name="insights")
    op.drop_table("insights")
    op.drop_index("idx_diffs_competitor", table_name="diffs")
    op.drop_table("diffs")
    op.drop_index("idx_snapshots_competitor", table_name="snapshots")
    op.drop_table("snapshots")
    op.drop_index("idx_competitors_org", table_name="competitors")
    op.drop_table("competitors")
    op.drop_table("user_organizations")
    op.drop_index("idx_jobs_status", table_name="jobs")
    op.drop_table("jobs")
    op.drop_table("organizations")
    op.drop_index("idx_users_email", table_name="users")
    op.drop_table("users")
    membership_role.drop(op.get_bind(), checkfirst=True)
