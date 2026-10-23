"""Sender de desarrollo: "envía" el email imprimiéndolo. Cambiar por SMTP/SES después."""
import logging

from notification_service.application.ports.notification_sender import NotificationSender
from notification_service.domain.entities.notification import Notification

logger = logging.getLogger("notification_service.email")


class ConsoleEmailSender(NotificationSender):
    def send(self, notification: Notification) -> None:
        logger.warning(
            "EMAIL -> %s | %s | %s", notification.recipient, notification.subject, notification.body
        )
