import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Index, text
from sqlmodel import Field, SQLModel

from payment_service.shared.config import DB_SCHEMA
from payment_service.shared.time import utc_now


class PaymentModel(SQLModel, table=True):
    __tablename__ = "payments"
    __table_args__ = (
        # Integridad: como máximo UN pago aprobado por reserva (índice único parcial).
        Index(
            "uq_payments_one_approved_per_booking",
            "booking_id",
            unique=True,
            postgresql_where=text("status = 'APPROVED'"),
        ),
        {"schema": DB_SCHEMA},
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    booking_id: uuid.UUID = Field(index=True)  # vive en booking-service: sin FK
    user_id: uuid.UUID
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    method: str = Field(max_length=20)
    status: str = Field(max_length=20)
    failure_reason: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
    processed_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))
