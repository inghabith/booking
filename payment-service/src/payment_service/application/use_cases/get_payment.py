from uuid import UUID

from payment_service.domain.entities.payment import Payment
from payment_service.domain.exceptions import PaymentNotFoundError
from payment_service.domain.repositories.payment_repository import PaymentRepository


class GetPayment:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def execute(self, payment_id: UUID) -> Payment:
        payment = self.payment_repository.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError(payment_id)
        return payment
