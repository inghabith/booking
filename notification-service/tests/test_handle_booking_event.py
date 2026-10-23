import json
import uuid

import pytest

from notification_service.application.use_cases.handle_booking_event import (
    HandleBookingEvent,
    RecipientNotFoundError,
)
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.domain.exceptions import UnsupportedEventError
from notification_service.presentation.consumers.message_parser import parse_message
from tests.fakes import FakeUserDirectory, InMemoryNotificationRepository, SpySender, contact


def message(name="booking.confirmed", user_id=None):
    """Mismo formato que publica booking-service."""
    return json.dumps(
        {
            "event": name,
            "event_id": str(uuid.uuid4()),
            "occurred_at": "2026-11-01T12:00:00+00:00",
            "data": {
                "booking_id": str(uuid.uuid4()),
                "user_id": str(user_id or uuid.uuid4()),
                "resource_id": str(uuid.uuid4()),
                "start_at": "2026-11-03 15:00:00+00:00",
                "end_at": "2026-11-03 17:00:00+00:00",
                "total_price": "100000.00",
            },
        }
    ).encode()


@pytest.fixture
def setup():
    user_id = uuid.uuid4()
    sender = SpySender()
    use_case = HandleBookingEvent(
        FakeUserDirectory({user_id: contact()}),
        SendNotification(InMemoryNotificationRepository(), sender),
    )
    return user_id, sender, use_case


def test_reserva_confirmada_envia_email(setup):
    user_id, sender, use_case = setup
    notification = use_case.execute(parse_message(message(user_id=user_id)))
    assert notification.recipient == "ana@mail.com"
    assert "confirmada" in notification.subject
    assert len(sender.sent) == 1


def test_reserva_cancelada(setup):
    user_id, _, use_case = setup
    notification = use_case.execute(parse_message(message("booking.cancelled", user_id)))
    assert "cancelada" in notification.subject


def test_usuario_desconocido(setup):
    _, _, use_case = setup
    with pytest.raises(RecipientNotFoundError):
        use_case.execute(parse_message(message()))


def test_evento_no_soportado(setup):
    user_id, _, use_case = setup
    with pytest.raises(UnsupportedEventError):
        use_case.execute(parse_message(message("booking.exploded", user_id)))
