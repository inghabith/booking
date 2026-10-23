import uuid
from decimal import Decimal

import pytest

from booking_service.domain.entities.booking import Booking, BookingStatus
from booking_service.domain.events import BookingCancelled, BookingConfirmed
from booking_service.domain.exceptions import (
    InvalidBookingError,
    InvalidBookingTransitionError,
)
from booking_service.domain.value_objects.time_slot import TimeSlot
from tests.conftest import NOW, at


def schedule(start=10, end=12, attendees=2, price="50000.00", capacity=8, now=NOW):
    return Booking.schedule(
        user_id=uuid.uuid4(),
        resource_id=uuid.uuid4(),
        slot=TimeSlot(at(start), at(end)),
        price_per_hour=Decimal(price),
        resource_capacity=capacity,
        attendees=attendees,
        now=now,
    )


def test_calcula_el_total_con_el_precio_del_recurso():
    booking = Booking.schedule(
        user_id=uuid.uuid4(),
        resource_id=uuid.uuid4(),
        slot=TimeSlot(at(10), at(11, 30)),
        price_per_hour=Decimal("50000.00"),
        resource_capacity=8,
        attendees=1,
        now=NOW,
    )
    assert booking.total_price == Decimal("75000.00")
    assert booking.status == BookingStatus.PENDING


def test_reserva_en_el_pasado_falla():
    with pytest.raises(InvalidBookingError):
        schedule(now=at(23))


def test_supera_capacidad_falla():
    with pytest.raises(InvalidBookingError):
        schedule(attendees=9, capacity=8)


def test_confirmar_emite_evento_una_sola_vez():
    booking = schedule()
    booking.confirm()
    events = booking.pull_events()
    assert booking.status == BookingStatus.CONFIRMED
    assert len(events) == 1 and isinstance(events[0], BookingConfirmed)
    assert booking.pull_events() == []


def test_no_se_confirma_dos_veces():
    booking = schedule()
    booking.confirm()
    with pytest.raises(InvalidBookingTransitionError):
        booking.confirm()


def test_cancelar_emite_evento():
    booking = schedule()
    booking.cancel(now=NOW)
    assert booking.status == BookingStatus.CANCELLED
    assert isinstance(booking.pull_events()[0], BookingCancelled)


def test_no_se_cancela_una_reserva_que_ya_empezo():
    booking = schedule()
    with pytest.raises(InvalidBookingTransitionError):
        booking.cancel(now=at(11))


def test_cancelada_no_genera_conflicto():
    a = schedule()
    b = Booking(
        user_id=uuid.uuid4(),
        resource_id=a.resource_id,
        slot=a.slot,
        total_price=Decimal("0"),
    )
    assert a.conflicts_with(b)
    b.cancel(now=NOW)
    assert not a.conflicts_with(b)
