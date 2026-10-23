import uuid
from dataclasses import replace

import pytest

from booking_service.application.dtos import CreateBookingCommand
from booking_service.application.use_cases.cancel_booking import CancelBooking
from booking_service.application.use_cases.confirm_booking import ConfirmBooking
from booking_service.application.use_cases.create_booking import CreateBooking
from booking_service.domain.events import BookingConfirmed
from booking_service.domain.exceptions import (
    BookingConflictError,
    ResourceNotFoundError,
    ResourceUnavailableError,
    UserNotFoundError,
)
from tests.conftest import at
from tests.fakes import FakeResourceGateway


@pytest.fixture
def create(repo, resources, users, clock):
    return CreateBooking(repo, resources, users, clock=clock)


def cmd(user_id, room, start=10, end=12, **kw):
    return CreateBookingCommand(
        user_id=user_id, resource_id=room.id, start_at=at(start), end_at=at(end), **kw
    )


def test_crea_reserva(create, user_id, room, repo):
    booking = create.execute(cmd(user_id, room))
    assert repo.get_by_id(booking.id) is booking


def test_solapamiento_falla(create, user_id, room):
    create.execute(cmd(user_id, room, 10, 12))
    with pytest.raises(BookingConflictError):
        create.execute(cmd(user_id, room, 11, 13))


def test_reservas_contiguas_son_validas(create, user_id, room):
    create.execute(cmd(user_id, room, 10, 11))
    create.execute(cmd(user_id, room, 11, 12))


def test_otro_recurso_mismo_horario_es_valido(repo, users, clock, user_id, room):
    other = replace(room, id=uuid.uuid4(), name="Sala Sierra")
    use_case = CreateBooking(repo, FakeResourceGateway(room, other), users, clock=clock)
    use_case.execute(cmd(user_id, room))
    use_case.execute(cmd(user_id, other))


def test_cancelar_libera_el_horario(create, repo, publisher, clock, user_id, room):
    booking = create.execute(cmd(user_id, room))
    CancelBooking(repo, publisher, clock=clock).execute(booking.id)
    create.execute(cmd(user_id, room))


def test_usuario_inexistente(create, room):
    with pytest.raises(UserNotFoundError):
        create.execute(cmd(uuid.uuid4(), room))


def test_recurso_inexistente(create, user_id, room):
    with pytest.raises(ResourceNotFoundError):
        create.execute(cmd(user_id, replace(room, id=uuid.uuid4())))


def test_recurso_inactivo(repo, users, clock, user_id, room):
    inactive = replace(room, is_active=False)
    use_case = CreateBooking(repo, FakeResourceGateway(inactive), users, clock=clock)
    with pytest.raises(ResourceUnavailableError):
        use_case.execute(cmd(user_id, inactive))


def test_confirmar_publica_evento(create, repo, publisher, user_id, room):
    booking = create.execute(cmd(user_id, room))
    ConfirmBooking(repo, publisher).execute(booking.id)
    assert [type(e) for e in publisher.events] == [BookingConfirmed]
