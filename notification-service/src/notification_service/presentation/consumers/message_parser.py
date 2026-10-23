"""Traduce el mensaje crudo de RabbitMQ a un DTO de aplicación."""
import json
from uuid import UUID

from notification_service.application.dtos import IntegrationEvent


def parse_message(body: bytes) -> IntegrationEvent:
    message = json.loads(body)
    return IntegrationEvent(
        name=message["event"],
        event_id=UUID(message["event_id"]),
        data=message["data"],
    )
