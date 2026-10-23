import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from booking_service.application.ports.resource_gateway import ResourceSnapshot
from tests.fakes import (
    FakeResourceGateway,
    FakeUserGateway,
    InMemoryBookingRepository,
    SpyEventPublisher,
)

# Reloj fijo: los tests no dependen de la hora real.
NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


def at(hour, minute=0, day=3):
    return datetime(2026, 11, day, hour, minute, tzinfo=timezone.utc)


@pytest.fixture
def user_id():
    return uuid.uuid4()


@pytest.fixture
def room():
    return ResourceSnapshot(
        id=uuid.uuid4(),
        name="Sala Caribe",
        capacity=8,
        price_per_hour=Decimal("50000.00"),
        is_active=True,
    )


@pytest.fixture
def repo():
    return InMemoryBookingRepository()


@pytest.fixture
def publisher():
    return SpyEventPublisher()


@pytest.fixture
def resources(room):
    return FakeResourceGateway(room)


@pytest.fixture
def users(user_id):
    return FakeUserGateway(user_id)


@pytest.fixture
def clock():
    return lambda: NOW


@pytest.fixture
def one_hour():
    return timedelta(hours=1)
