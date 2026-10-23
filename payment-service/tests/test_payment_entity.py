import uuid
from decimal import Decimal

import pytest

from payment_service.domain.entities.payment import Payment, PaymentMethod, PaymentStatus
from payment_service.domain.exceptions import (
    InvalidPaymentError,
    InvalidPaymentTransitionError,
)
from payment_service.shared.time import utc_now


def make(amount="1000"):
    return Payment(
        booking_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        amount=Decimal(amount),
        method=PaymentMethod.CARD,
    )


def test_monto_cero_falla():
    with pytest.raises(InvalidPaymentError):
        make("0")


def test_no_se_procesa_dos_veces():
    payment = make()
    payment.approve(utc_now())
    assert payment.status == PaymentStatus.APPROVED
    with pytest.raises(InvalidPaymentTransitionError):
        payment.decline("x", utc_now())
