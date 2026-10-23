import uuid
from decimal import Decimal

import pytest

from payment_service.application.ports.booking_gateway import BookingSnapshot
from payment_service.application.use_cases.create_payment import CreatePayment
from payment_service.infrastructure.processors.simulated_payment_processor import (
    SimulatedPaymentProcessor,
)
from tests.fakes import FakeBookingGateway, InMemoryPaymentRepository


@pytest.fixture
def booking():
    return BookingSnapshot(
        id=uuid.uuid4(), user_id=uuid.uuid4(), status="PENDING", total_price=Decimal("100000.00")
    )


@pytest.fixture
def repo():
    return InMemoryPaymentRepository()


@pytest.fixture
def bookings(booking):
    return FakeBookingGateway(booking)


@pytest.fixture
def create_payment(repo, bookings):
    return CreatePayment(repo, bookings, SimulatedPaymentProcessor())
