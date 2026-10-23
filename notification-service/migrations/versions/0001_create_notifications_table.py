"""create notifications table

Revision ID: 0001_notifications
Revises:
Create Date: 2026-10-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_notifications"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "notifications"


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("recipient", sa.String(254), nullable=False),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("body", sa.String(2000), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("reference_id", sa.Uuid(), nullable=True),
        sa.Column("event_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("error", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("event_id", name="uq_notifications_event_id"),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_notifications_notifications_user_id", "notifications", ["user_id"], schema=SCHEMA
    )
    op.create_index(
        "ix_notifications_notifications_reference_id",
        "notifications",
        ["reference_id"],
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("notifications", schema=SCHEMA)
