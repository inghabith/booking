"""Eventos de dominio: hechos que ya ocurrieron. Otros servicios reaccionan a ellos."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from booking_service.shared.time import utc_now


@dataclass(frozen=True)
class BookingConfirmed:
    name: ClassVar[str] = "booking.confirmed"

    booking_id: uuid.UUID
    user_id: uuid.UUID
    resource_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    total_price: Decimal
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True)
class BookingCancelled:
    name: ClassVar[str] = "booking.cancelled"

    booking_id: uuid.UUID
    user_id: uuid.UUID
    resource_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=utc_now)


DomainEvent = BookingConfirmed | BookingCancelled
