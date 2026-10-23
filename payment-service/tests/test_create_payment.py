import uuid
from dataclasses import replace

import pytest

from payment_service.application.dtos import CreatePaymentCommand
from payment_service.domain.entities.payment import PaymentMethod, PaymentStatus
from payment_service.domain.exceptions import (
    BookingNotFoundError,
    BookingNotPayableError,
    PaymentAlreadyApprovedError,
)
from tests.fakes import FakeBookingGateway


def cmd(booking_id, token="tok_visa"):
    return CreatePaymentCommand(booking_id=booking_id, method=PaymentMethod.CARD, payment_token=token)


def test_pago_aprobado_confirma_la_reserva(create_payment, booking, bookings):
    payment = create_payment.execute(cmd(booking.id))
    assert payment.status == PaymentStatus.APPROVED
    assert payment.amount == booking.total_price  # el monto viene de booking
    assert bookings.confirmed == [booking.id]


def test_pago_rechazado_no_confirma(create_payment, booking, bookings):
    payment = create_payment.execute(cmd(booking.id, "tok_declined"))
    assert payment.status == PaymentStatus.DECLINED
    assert payment.failure_reason == "Fondos insuficientes"
    assert bookings.confirmed == []


def test_se_puede_reintentar_tras_rechazo(create_payment, booking):
    create_payment.execute(cmd(booking.id, "tok_declined"))
    assert create_payment.execute(cmd(booking.id)).status == PaymentStatus.APPROVED


def test_no_se_paga_dos_veces(create_payment, booking):
    create_payment.execute(cmd(booking.id))
    with pytest.raises(PaymentAlreadyApprovedError):
        create_payment.execute(cmd(booking.id))


def test_reserva_inexistente(create_payment):
    with pytest.raises(BookingNotFoundError):
        create_payment.execute(cmd(uuid.uuid4()))


def test_reserva_cancelada_no_se_paga(repo, booking):
    from payment_service.application.use_cases.create_payment import CreatePayment
    from payment_service.infrastructure.processors.simulated_payment_processor import (
        SimulatedPaymentProcessor,
    )

    cancelled = replace(booking, status="CANCELLED")
    use_case = CreatePayment(repo, FakeBookingGateway(cancelled), SimulatedPaymentProcessor())
    with pytest.raises(BookingNotPayableError):
        use_case.execute(cmd(cancelled.id))
