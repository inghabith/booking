"""Construcción de casos de uso fuera de FastAPI (el worker de RabbitMQ)."""
from sqlmodel import Session

from notification_service.application.use_cases.handle_booking_event import HandleBookingEvent
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.infrastructure.clients.http_user_directory import HttpUserDirectory
from notification_service.infrastructure.persistence.repositories.sqlmodel_notification_repository import (
    SQLModelNotificationRepository,
)
from notification_service.infrastructure.senders.console_email_sender import ConsoleEmailSender
from notification_service.shared import config


def build_handle_booking_event(session: Session) -> HandleBookingEvent:
    send = SendNotification(SQLModelNotificationRepository(session), ConsoleEmailSender())
    directory = HttpUserDirectory(config.USERS_SERVICE_URL, config.HTTP_TIMEOUT_SECONDS)
    return HandleBookingEvent(directory, send)
