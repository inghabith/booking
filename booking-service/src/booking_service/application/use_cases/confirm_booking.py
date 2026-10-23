from uuid import UUID

from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.domain.entities.booking import Booking
from booking_service.domain.exceptions import BookingNotFoundError
from booking_service.domain.repositories.booking_repository import BookingRepository


class ConfirmBooking:
    """Lo invoca payment-service cuando un pago es aprobado."""

    def __init__(self, booking_repository: BookingRepository, event_publisher: EventPublisher):
        self.booking_repository = booking_repository
        self.event_publisher = event_publisher

    def execute(self, booking_id: UUID) -> Booking:
        booking = self.booking_repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError(booking_id)

        booking.confirm()
        self.booking_repository.update(booking)

        # Nota: se publica antes del commit. Si el commit fallara, el evento ya salió.
        # La solución robusta (outbox pattern) se ve en la sesión de mensajería.
        for event in booking.pull_events():
            self.event_publisher.publish(event)

        return booking
