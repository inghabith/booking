"""Puerto hacia booking-service."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class BookingSnapshot:
    id: UUID
    user_id: UUID
    status: str
    total_price: Decimal


class BookingGateway(ABC):
    @abstractmethod
    def get(self, booking_id: UUID) -> BookingSnapshot | None: ...

    @abstractmethod
    def confirm(self, booking_id: UUID) -> None: ...
