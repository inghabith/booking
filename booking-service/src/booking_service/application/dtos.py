from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from booking_service.domain.entities.booking import BookingStatus


@dataclass(frozen=True)
class CreateBookingCommand:
    user_id: UUID
    resource_id: UUID
    start_at: datetime
    end_at: datetime
    attendees: int = 1


@dataclass(frozen=True)
class BookingFilters:
    user_id: UUID | None = None
    resource_id: UUID | None = None
    status: BookingStatus | None = None
