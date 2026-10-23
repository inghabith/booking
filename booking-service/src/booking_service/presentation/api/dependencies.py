"""Composition root: aquí se eligen los adaptadores concretos."""
from functools import lru_cache

from fastapi import Depends

from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.application.ports.resource_gateway import ResourceGateway
from booking_service.application.ports.user_gateway import UserGateway
from booking_service.application.use_cases.cancel_booking import CancelBooking
from booking_service.application.use_cases.confirm_booking import ConfirmBooking
from booking_service.application.use_cases.create_booking import CreateBooking
from booking_service.application.use_cases.get_booking import GetBooking
from booking_service.application.use_cases.list_bookings import ListBookings
from booking_service.domain.repositories.booking_repository import BookingRepository
from booking_service.infrastructure.clients.http_resource_gateway import HttpResourceGateway
from booking_service.infrastructure.clients.http_user_gateway import HttpUserGateway
from booking_service.infrastructure.database.session import get_session
from booking_service.infrastructure.messaging.logging_event_publisher import (
    LoggingEventPublisher,
)
from booking_service.infrastructure.messaging.rabbitmq_event_publisher import (
    RabbitMQEventPublisher,
)
from booking_service.infrastructure.persistence.repositories.sqlmodel_booking_repository import (
    SQLModelBookingRepository,
)
from booking_service.shared import config


def get_booking_repository(
    session=Depends(get_session, scope="function"),
) -> BookingRepository:
    return SQLModelBookingRepository(session)


def get_resource_gateway() -> ResourceGateway:
    return HttpResourceGateway(config.RESOURCES_SERVICE_URL, config.HTTP_TIMEOUT_SECONDS)


def get_user_gateway() -> UserGateway:
    return HttpUserGateway(config.USERS_SERVICE_URL, config.HTTP_TIMEOUT_SECONDS)


@lru_cache
def get_event_publisher() -> EventPublisher:
    if config.EVENT_PUBLISHER == "rabbitmq":
        return RabbitMQEventPublisher(config.RABBITMQ_URL, config.EVENTS_EXCHANGE)
    return LoggingEventPublisher()


def get_create_booking(
    repository=Depends(get_booking_repository),
    resources=Depends(get_resource_gateway),
    users=Depends(get_user_gateway),
) -> CreateBooking:
    return CreateBooking(repository, resources, users)


def get_get_booking(repository=Depends(get_booking_repository)) -> GetBooking:
    return GetBooking(repository)


def get_list_bookings(repository=Depends(get_booking_repository)) -> ListBookings:
    return ListBookings(repository)


def get_confirm_booking(
    repository=Depends(get_booking_repository), publisher=Depends(get_event_publisher)
) -> ConfirmBooking:
    return ConfirmBooking(repository, publisher)


def get_cancel_booking(
    repository=Depends(get_booking_repository), publisher=Depends(get_event_publisher)
) -> CancelBooking:
    return CancelBooking(repository, publisher)
