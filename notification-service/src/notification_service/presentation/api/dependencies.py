"""Composition root de la API."""
from fastapi import Depends

from notification_service.application.ports.notification_sender import NotificationSender
from notification_service.application.use_cases.get_notification import GetNotification
from notification_service.application.use_cases.list_notifications import ListNotifications
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)
from notification_service.infrastructure.database.session import get_session
from notification_service.infrastructure.persistence.repositories.sqlmodel_notification_repository import (
    SQLModelNotificationRepository,
)
from notification_service.infrastructure.senders.console_email_sender import ConsoleEmailSender


def get_notification_repository(
    session=Depends(get_session, scope="function"),
) -> NotificationRepository:
    return SQLModelNotificationRepository(session)


def get_sender() -> NotificationSender:
    return ConsoleEmailSender()


def get_send_notification(
    repository=Depends(get_notification_repository), sender=Depends(get_sender)
) -> SendNotification:
    return SendNotification(repository, sender)


def get_get_notification(repository=Depends(get_notification_repository)) -> GetNotification:
    return GetNotification(repository)


def get_list_notifications(
    repository=Depends(get_notification_repository),
) -> ListNotifications:
    return ListNotifications(repository)
