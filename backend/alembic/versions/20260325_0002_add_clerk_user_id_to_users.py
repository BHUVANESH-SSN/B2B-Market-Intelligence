"""add clerk user id

Revision ID: 20260325_0002
Revises: 20260325_0001
Create Date: 2026-03-25 12:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260325_0002"
down_revision = "20260325_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("clerk_user_id", sa.String(length=255), nullable=True))
    op.create_index("idx_users_clerk_user_id", "users", ["clerk_user_id"], unique=True)


def downgrade() -> None:
    op.drop_index("idx_users_clerk_user_id", table_name="users")
    op.drop_column("users", "clerk_user_id")
