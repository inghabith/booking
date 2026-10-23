"""create resources table

Revision ID: 0001_resources
Revises:
Create Date: 2026-10-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_resources"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "resources"


def upgrade() -> None:
    op.create_table(
        "resources",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("resource_type", sa.String(30), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("price_per_hour", sa.Numeric(12, 2), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("description", sa.String(1000), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("name", name="uq_resources_name"),
        # Defensa en la base además de la validación del dominio.
        sa.CheckConstraint("capacity > 0", name="ck_resources_capacity_positive"),
        sa.CheckConstraint("price_per_hour >= 0", name="ck_resources_price_non_negative"),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_resources_resources_resource_type", "resources", ["resource_type"], schema=SCHEMA
    )


def downgrade() -> None:
    op.drop_index("ix_resources_resources_resource_type", table_name="resources", schema=SCHEMA)
    op.drop_table("resources", schema=SCHEMA)
