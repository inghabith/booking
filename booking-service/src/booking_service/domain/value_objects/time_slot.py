"""Value object: un intervalo [inicio, fin). Inmutable y siempre válido."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import ClassVar

from booking_service.domain.exceptions import InvalidTimeSlotError


@dataclass(frozen=True)
class TimeSlot:
    start_at: datetime
    end_at: datetime

    MIN_DURATION: ClassVar[timedelta] = timedelta(minutes=30)
    MAX_DURATION: ClassVar[timedelta] = timedelta(hours=12)

    def __post_init__(self):
        if self.start_at.tzinfo is None or self.end_at.tzinfo is None:
            raise InvalidTimeSlotError("Las fechas deben incluir zona horaria")
        if self.end_at <= self.start_at:
            raise InvalidTimeSlotError("La hora de fin debe ser posterior a la de inicio")
        if self.duration < self.MIN_DURATION:
            raise InvalidTimeSlotError("La reserva debe durar al menos 30 minutos")
        if self.duration > self.MAX_DURATION:
            raise InvalidTimeSlotError("La reserva no puede durar más de 12 horas")

    @property
    def duration(self) -> timedelta:
        return self.end_at - self.start_at

    @property
    def hours(self) -> Decimal:
        return Decimal(int(self.duration.total_seconds())) / Decimal(3600)

    def overlaps(self, other: "TimeSlot") -> bool:
        # Intervalos semiabiertos: 10:00-11:00 y 11:00-12:00 NO se solapan.
        return self.start_at < other.end_at and other.start_at < self.end_at
