"""Entidad Booking: reglas de reserva y su máquina de estados.

PENDING --confirm()--> CONFIRMED
PENDING/CONFIRMED --cancel()--> CANCELLED
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum

from booking_service.domain.events import BookingCancelled, BookingConfirmed, DomainEvent
from booking_service.domain.exceptions import (
    InvalidBookingError,
    InvalidBookingTransitionError,
)
from booking_service.domain.value_objects.time_slot import TimeSlot
from booking_service.shared.time import utc_now


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class Booking:
    user_id: uuid.UUID
    resource_id: uuid.UUID
    slot: TimeSlot
    total_price: Decimal
    attendees: int = 1
    status: BookingStatus = BookingStatus.PENDING
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime | None = None
    _events: list = field(default_factory=list, repr=False, compare=False)

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = self.created_at
        if self.attendees <= 0:
            raise InvalidBookingError("Debe haber al menos un asistente")
        if self.total_price < 0:
            raise InvalidBookingError("El total no puede ser negativo")

    # ---------- creación ----------
    @classmethod
    def schedule(
        cls,
        user_id: uuid.UUID,
        resource_id: uuid.UUID,
        slot: TimeSlot,
        price_per_hour: Decimal,
        resource_capacity: int,
        attendees: int,
        now: datetime,
    ) -> "Booking":
        """Crea una reserva nueva aplicando las reglas de negocio de creación."""
        if slot.start_at <= now:
            raise InvalidBookingError("La reserva debe empezar en el futuro")
        if attendees > resource_capacity:
            raise InvalidBookingError(
                f"El recurso admite máximo {resource_capacity} asistentes"
            )

        # El precio lo calcula el sistema a partir del recurso, nunca el cliente.
        total = (Decimal(price_per_hour) * slot.hours).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return cls(
            user_id=user_id,
            resource_id=resource_id,
            slot=slot,
            total_price=total,
            attendees=attendees,
        )

    # ---------- reglas ----------
    @property
    def is_active(self) -> bool:
        return self.status != BookingStatus.CANCELLED

    def conflicts_with(self, other: "Booking") -> bool:
        return (
            self.id != other.id
            and self.resource_id == other.resource_id
            and self.is_active
            and other.is_active
            and self.slot.overlaps(other.slot)
        )

    # ---------- transiciones ----------
    def confirm(self) -> None:
        if self.status != BookingStatus.PENDING:
            raise InvalidBookingTransitionError(
                f"Solo se puede confirmar una reserva PENDING (estado actual: {self.status.value})"
            )
        self.status = BookingStatus.CONFIRMED
        self.updated_at = utc_now()
        self._events.append(
            BookingConfirmed(
                booking_id=self.id,
                user_id=self.user_id,
                resource_id=self.resource_id,
                start_at=self.slot.start_at,
                end_at=self.slot.end_at,
                total_price=self.total_price,
            )
        )

    def cancel(self, now: datetime) -> None:
        if self.status == BookingStatus.CANCELLED:
            raise InvalidBookingTransitionError("La reserva ya está cancelada")
        if self.slot.start_at <= now:
            raise InvalidBookingTransitionError(
                "No se puede cancelar una reserva que ya empezó"
            )
        self.status = BookingStatus.CANCELLED
        self.updated_at = utc_now()
        self._events.append(
            BookingCancelled(
                booking_id=self.id,
                user_id=self.user_id,
                resource_id=self.resource_id,
                start_at=self.slot.start_at,
                end_at=self.slot.end_at,
            )
        )

    def pull_events(self) -> list[DomainEvent]:
        """Entrega los eventos pendientes y los limpia (se publican una sola vez)."""
        events, self._events = self._events, []
        return events
