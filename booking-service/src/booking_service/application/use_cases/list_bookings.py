from booking_service.application.dtos import BookingFilters
from booking_service.domain.entities.booking import Booking
from booking_service.domain.repositories.booking_repository import BookingRepository


class ListBookings:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def execute(self, filters: BookingFilters) -> list[Booking]:
        return self.booking_repository.list(
            user_id=filters.user_id,
            resource_id=filters.resource_id,
            status=filters.status,
        )
