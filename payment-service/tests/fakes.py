from payment_service.application.ports.booking_gateway import BookingGateway
from payment_service.domain.entities.payment import PaymentStatus
from payment_service.domain.repositories.payment_repository import PaymentRepository


class InMemoryPaymentRepository(PaymentRepository):
    def __init__(self):
        self.payments = {}

    def add(self, payment):
        self.payments[payment.id] = payment
        return payment

    def get_by_id(self, payment_id):
        return self.payments.get(payment_id)

    def get_approved_for_booking(self, booking_id):
        return next(
            (
                p
                for p in self.payments.values()
                if p.booking_id == booking_id and p.status == PaymentStatus.APPROVED
            ),
            None,
        )

    def list(self, booking_id=None):
        return [p for p in self.payments.values() if booking_id in (None, p.booking_id)]


class FakeBookingGateway(BookingGateway):
    def __init__(self, *bookings):
        self.bookings = {b.id: b for b in bookings}
        self.confirmed = []

    def get(self, booking_id):
        return self.bookings.get(booking_id)

    def confirm(self, booking_id):
        self.confirmed.append(booking_id)
