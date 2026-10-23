import logging

from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.domain.events import DomainEvent
from booking_service.infrastructure.messaging.serialization import event_to_json

logger = logging.getLogger("booking_service.events")


class LoggingEventPublisher(EventPublisher):
    """Útil en desarrollo sin RabbitMQ: solo imprime el evento."""

    def publish(self, event: DomainEvent) -> None:
        logger.warning("Evento publicado: %s", event_to_json(event))
