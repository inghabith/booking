"""Tabla de reservas.

La restricción de NO solapamiento (EXCLUDE USING gist) no se puede declarar
con SQLModel: vive en la migración 0001 y es la garantía final de la regla.
"""
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from booking_service.shared.config import DB_SCHEMA
from booking_service.shared.time import utc_now


class BookingModel(SQLModel, table=True):
    __tablename__ = "bookings"
    __table_args__ = {"schema": DB_SCHEMA}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Viven en otros servicios: solo guardamos el id, SIN foreign key.
    user_id: uuid.UUID = Field(index=True)
    resource_id: uuid.UUID = Field(index=True)

    start_at: datetime = Field(sa_type=DateTime(timezone=True))
    end_at: datetime = Field(sa_type=DateTime(timezone=True))
    attendees: int = Field(default=1)
    total_price: Decimal = Field(max_digits=12, decimal_places=2)
    status: str = Field(max_length=20)

    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
