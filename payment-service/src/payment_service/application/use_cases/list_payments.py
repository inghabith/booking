from uuid import UUID

from payment_service.domain.entities.payment import Payment
from payment_service.domain.repositories.payment_repository import PaymentRepository


class ListPayments:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def execute(self, booking_id: UUID | None = None) -> list[Payment]:
        return self.payment_repository.list(booking_id=booking_id)
