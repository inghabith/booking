"""create payments table

Revision ID: 0001_payments
Revises:
Create Date: 2026-10-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_payments"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "payments"


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("booking_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("method", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("failure_reason", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("amount > 0", name="ck_payments_amount_positive"),
        sa.CheckConstraint(
            "status IN ('PENDING', 'APPROVED', 'DECLINED')", name="ck_payments_status"
        ),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_payments_payments_booking_id", "payments", ["booking_id"], schema=SCHEMA
    )
    # Integridad de la transacción: máximo un pago APPROVED por reserva.
    op.create_index(
        "uq_payments_one_approved_per_booking",
        "payments",
        ["booking_id"],
        unique=True,
        schema=SCHEMA,
        postgresql_where=sa.text("status = 'APPROVED'"),
    )


def downgrade() -> None:
    op.drop_table("payments", schema=SCHEMA)
