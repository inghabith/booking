from uuid import UUID

from booking_service.domain.entities.booking import Booking
from booking_service.domain.exceptions import BookingNotFoundError
from booking_service.domain.repositories.booking_repository import BookingRepository


class GetBooking:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def execute(self, booking_id: UUID) -> Booking:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError(booking_id)
        return booking
