from collections.abc import Callable
from datetime import datetime

from payment_service.application.dtos import CreatePaymentCommand
from payment_service.application.ports.booking_gateway import BookingGateway
from payment_service.application.ports.payment_processor import PaymentProcessor
from payment_service.domain.entities.payment import Payment
from payment_service.domain.exceptions import (
    BookingNotFoundError,
    BookingNotPayableError,
    PaymentAlreadyApprovedError,
)
from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.shared.time import utc_now


class CreatePayment:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        booking_gateway: BookingGateway,
        payment_processor: PaymentProcessor,
        clock: Callable[[], datetime] = utc_now,
    ):
        self.payment_repository = payment_repository
        self.booking_gateway = booking_gateway
        self.payment_processor = payment_processor
        self.clock = clock

    def execute(self, command: CreatePaymentCommand) -> Payment:
        booking = self.booking_gateway.get(command.booking_id)
        if booking is None:
            raise BookingNotFoundError(command.booking_id)
        if booking.status != "PENDING":
            raise BookingNotPayableError(booking.id, booking.status)
        if self.payment_repository.get_approved_for_booking(booking.id):
            raise PaymentAlreadyApprovedError(booking.id)

        # El monto sale de booking-service, nunca del cliente.
        payment = Payment(
            booking_id=booking.id,
            user_id=booking.user_id,
            amount=booking.total_price,
            method=command.method,
        )

        result = self.payment_processor.charge(
            payment.amount, payment.method, command.payment_token
        )
        if result.approved:
            payment.approve(now=self.clock())
        else:
            payment.decline(result.reason or "Pago rechazado", now=self.clock())

        self.payment_repository.add(payment)

        if payment.is_approved:
            # Llamada síncrona: si booking-service falla, la transacción del pago
            # hace rollback. Idempotencia y reintentos se ven en sesiones siguientes.
            self.booking_gateway.confirm(booking.id)

        return payment
