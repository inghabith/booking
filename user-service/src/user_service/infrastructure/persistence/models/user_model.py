"""Modelo de persistencia: forma de la tabla. Solo lo conoce infrastructure."""
import uuid
from datetime import date, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, UniqueConstraint

from user_service.shared.config import DB_SCHEMA
from user_service.shared.time import utc_now


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "identification_type", "identification_number", name="uq_users_identification"
        ),
        {"schema": DB_SCHEMA},
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=120, index=True)
    email: str = Field(max_length=254, unique=True)
    identification_type: str = Field(max_length=20)
    identification_number: str = Field(max_length=30)
    birthday_date: date
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
