from datetime import datetime, timedelta

import pytest

from booking_service.domain.exceptions import InvalidTimeSlotError
from booking_service.domain.value_objects.time_slot import TimeSlot
from tests.conftest import at


def test_fin_antes_de_inicio_falla():
    with pytest.raises(InvalidTimeSlotError):
        TimeSlot(at(11), at(10))


def test_sin_zona_horaria_falla():
    with pytest.raises(InvalidTimeSlotError):
        TimeSlot(datetime(2026, 11, 3, 10), datetime(2026, 11, 3, 11))


def test_duracion_minima_y_maxima():
    with pytest.raises(InvalidTimeSlotError):
        TimeSlot(at(10), at(10, 15))
    with pytest.raises(InvalidTimeSlotError):
        TimeSlot(at(8), at(8) + timedelta(hours=13))


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ((10, 12), (11, 13), True),   # se cruzan
        ((10, 12), (10, 12), True),   # idénticos
        ((10, 14), (11, 12), True),   # uno contiene al otro
        ((10, 11), (11, 12), False),  # contiguos: permitido
        ((10, 11), (13, 14), False),  # separados
    ],
)
def test_overlaps(a, b, expected):
    slot_a = TimeSlot(at(a[0]), at(a[1]))
    slot_b = TimeSlot(at(b[0]), at(b[1]))
    assert slot_a.overlaps(slot_b) is expected
    assert slot_b.overlaps(slot_a) is expected
