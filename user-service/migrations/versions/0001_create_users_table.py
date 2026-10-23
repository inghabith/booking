"""create users table

Revision ID: 0001_users
Revises:
Create Date: 2026-10-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_users"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "users"


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("identification_type", sa.String(20), nullable=False),
        sa.Column("identification_number", sa.String(30), nullable=False),
        sa.Column("birthday_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint(
            "identification_type", "identification_number", name="uq_users_identification"
        ),
        schema=SCHEMA,
    )
    op.create_index("ix_users_users_name", "users", ["name"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_index("ix_users_users_name", table_name="users", schema=SCHEMA)
    op.drop_table("users", schema=SCHEMA)
