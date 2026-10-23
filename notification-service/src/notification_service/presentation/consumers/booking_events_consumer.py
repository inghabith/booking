"""Worker: consume booking.confirmed y booking.cancelled.

Es otro adaptador de ENTRADA (como un router): recibe un mensaje en vez de un
request HTTP y llama al mismo tipo de caso de uso.

    uv run python -m notification_service.presentation.consumers.booking_events_consumer
"""
import logging
import time

import pika

from notification_service.application.exceptions import ExternalServiceError
from notification_service.application.templates import SUPPORTED_EVENTS
from notification_service.infrastructure.container import build_handle_booking_event
from notification_service.infrastructure.database.session import session_scope
from notification_service.presentation.consumers.message_parser import parse_message
from notification_service.shared import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("notification_service.consumer")


def on_message(channel, method, properties, body) -> None:
    try:
        event = parse_message(body)
        with session_scope() as session:
            notification = build_handle_booking_event(session).execute(event)
        logger.info("Notificación %s para %s (%s)", notification.id, event.name, event.event_id)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except ExternalServiceError:
        # Fallo temporal (user-service caído): reintentar más tarde.
        logger.exception("Dependencia no disponible, se reencola el mensaje")
        time.sleep(2)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    except Exception:
        # Mensaje inválido: no reencolar para no bloquear la cola (dead-letter: sesión 7).
        logger.exception("No se pudo procesar el mensaje, se descarta")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def connect() -> pika.BlockingConnection:
    for attempt in range(1, 31):
        try:
            return pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_URL))
        except pika.exceptions.AMQPConnectionError:
            logger.info("RabbitMQ no disponible (intento %s), reintentando...", attempt)
            time.sleep(2)
    raise SystemExit("No fue posible conectar con RabbitMQ")


def main() -> None:
    connection = connect()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=config.BOOKING_EVENTS_EXCHANGE, exchange_type="topic", durable=True
    )
    channel.queue_declare(queue=config.BOOKING_EVENTS_QUEUE, durable=True)
    for routing_key in SUPPORTED_EVENTS:
        channel.queue_bind(
            queue=config.BOOKING_EVENTS_QUEUE,
            exchange=config.BOOKING_EVENTS_EXCHANGE,
            routing_key=routing_key,
        )

    channel.basic_qos(prefetch_count=10)
    channel.basic_consume(queue=config.BOOKING_EVENTS_QUEUE, on_message_callback=on_message)

    logger.info("Escuchando %s en la cola %s", SUPPORTED_EVENTS, config.BOOKING_EVENTS_QUEUE)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
