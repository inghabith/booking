from abc import ABC, abstractmethod
from uuid import UUID

from booking_service.domain.entities.booking import Booking, BookingStatus
from booking_service.domain.value_objects.time_slot import TimeSlot


class BookingRepository(ABC):
    @abstractmethod
    def add(self, booking: Booking) -> Booking:
        """Debe lanzar BookingConflictError si la base detecta un solapamiento."""

    @abstractmethod
    def update(self, booking: Booking) -> Booking: ...

    @abstractmethod
    def get_by_id(self, booking_id: UUID) -> Booking | None: ...

    @abstractmethod
    def find_active_overlapping(self, resource_id: UUID, slot: TimeSlot) -> list[Booking]: ...

    @abstractmethod
    def list(
        self,
        user_id: UUID | None = None,
        resource_id: UUID | None = None,
        status: BookingStatus | None = None,
    ) -> list[Booking]: ...
