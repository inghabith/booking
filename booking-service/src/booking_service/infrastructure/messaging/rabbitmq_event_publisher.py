"""Publica eventos en un exchange topic de RabbitMQ.

routing key = nombre del evento (booking.confirmed, booking.cancelled).
Cada consumidor (notification-service, ...) crea su propia cola y se suscribe.
"""
import pika

from booking_service.application.exceptions import ExternalServiceError
from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.domain.events import DomainEvent
from booking_service.infrastructure.messaging.serialization import event_to_json


class RabbitMQEventPublisher(EventPublisher):
    def __init__(self, url: str, exchange: str):
        self.url = url
        self.exchange = exchange

    def publish(self, event: DomainEvent) -> None:
        try:
            # Conexión por publicación: simple y suficiente para el taller.
            connection = pika.BlockingConnection(pika.URLParameters(self.url))
            try:
                channel = connection.channel()
                channel.exchange_declare(
                    exchange=self.exchange, exchange_type="topic", durable=True
                )
                channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=event.name,
                    body=event_to_json(event).encode("utf-8"),
                    properties=pika.BasicProperties(
                        content_type="application/json",
                        delivery_mode=2,  # persistente
                        message_id=str(event.event_id),
                    ),
                )
            finally:
                connection.close()
        except pika.exceptions.AMQPError as error:
            raise ExternalServiceError("RabbitMQ no está disponible") from error
