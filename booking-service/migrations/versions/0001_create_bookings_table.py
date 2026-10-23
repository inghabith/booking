"""create bookings table with no-overlap exclusion constraint

Revision ID: 0001_bookings
Revises:
Create Date: 2026-10-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_bookings"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "bookings"


def upgrade() -> None:
    # btree_gist permite combinar "=" sobre uuid con "&&" sobre rangos en un índice GiST.
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "bookings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attendees", sa.Integer(), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("end_at > start_at", name="ck_bookings_valid_range"),
        sa.CheckConstraint("attendees > 0", name="ck_bookings_attendees_positive"),
        sa.CheckConstraint(
            "status IN ('PENDING', 'CONFIRMED', 'CANCELLED')", name="ck_bookings_status"
        ),
        schema=SCHEMA,
    )
    op.create_index("ix_bookings_bookings_user_id", "bookings", ["user_id"], schema=SCHEMA)
    op.create_index(
        "ix_bookings_bookings_resource_id", "bookings", ["resource_id"], schema=SCHEMA
    )

    # REGLA CLAVE: dos reservas activas del mismo recurso no pueden solaparse.
    # '[)' = intervalo semiabierto, así 10:00-11:00 y 11:00-12:00 son válidas.
    op.execute(
        f"""
        ALTER TABLE {SCHEMA}.bookings
        ADD CONSTRAINT ex_bookings_no_overlap
        EXCLUDE USING gist (
            resource_id WITH =,
            tstzrange(start_at, end_at, '[)') WITH &&
        )
        WHERE (status <> 'CANCELLED')
        """
    )


def downgrade() -> None:
    op.drop_table("bookings", schema=SCHEMA)
