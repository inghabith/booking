"""Contrato de los mensajes: {"event", "event_id", "occurred_at", "data"}."""
import dataclasses
import json

from booking_service.domain.events import DomainEvent


def event_to_json(event: DomainEvent) -> str:
    data = dataclasses.asdict(event)
    message = {
        "event": event.name,
        "event_id": data.pop("event_id"),
        "occurred_at": data.pop("occurred_at"),
        "data": data,
    }
    return json.dumps(message, default=str)
