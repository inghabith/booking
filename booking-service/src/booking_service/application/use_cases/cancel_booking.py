from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.domain.entities.booking import Booking
from booking_service.domain.exceptions import BookingNotFoundError
from booking_service.domain.repositories.booking_repository import BookingRepository
from booking_service.shared.time import utc_now


class CancelBooking:
    def __init__(
        self,
        booking_repository: BookingRepository,
        event_publisher: EventPublisher,
        clock: Callable[[], datetime] = utc_now,
    ):
        self.booking_repository = booking_repository
        self.event_publisher = event_publisher
        self.clock = clock

    def execute(self, booking_id: UUID) -> Booking:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError(booking_id)

        booking.cancel(now=self.clock())
        self.booking_repository.update(booking)

        for event in booking.pull_events():
            self.event_publisher.publish(event)

        return booking
