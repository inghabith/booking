"""Textos de las notificaciones por tipo de evento (lógica pura, sin I/O)."""
from datetime import datetime

from notification_service.application.dtos import IntegrationEvent
from notification_service.application.ports.user_directory import UserContact
from notification_service.domain.exceptions import UnsupportedEventError

SUPPORTED_EVENTS = ("booking.confirmed", "booking.cancelled")


def _fmt(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M %Z").strip()


def render(event: IntegrationEvent, contact: UserContact) -> tuple[str, str]:
    data = event.data
    start, end = _fmt(data["start_at"]), _fmt(data["end_at"])

    if event.name == "booking.confirmed":
        subject = "Tu reserva está confirmada"
        body = (
            f"Hola {contact.name}, tu reserva {data['booking_id']} quedó confirmada "
            f"del {start} al {end}. Total pagado: {data['total_price']}."
        )
        return subject, body

    if event.name == "booking.cancelled":
        subject = "Tu reserva fue cancelada"
        body = (
            f"Hola {contact.name}, tu reserva {data['booking_id']} "
            f"del {start} al {end} fue cancelada."
        )
        return subject, body

    raise UnsupportedEventError(f"Evento no soportado: {event.name}")
