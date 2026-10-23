from collections.abc import Callable
from datetime import datetime

from notification_service.application.dtos import SendNotificationCommand
from notification_service.application.exceptions import DeliveryError
from notification_service.application.ports.notification_sender import NotificationSender
from notification_service.domain.entities.notification import Notification
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)
from notification_service.shared.time import utc_now


class SendNotification:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        sender: NotificationSender,
        clock: Callable[[], datetime] = utc_now,
    ):
        self.notification_repository = notification_repository
        self.sender = sender
        self.clock = clock

    def execute(self, command: SendNotificationCommand) -> Notification:
        # Idempotencia: RabbitMQ puede entregar el mismo mensaje más de una vez.
        if command.event_id is not None:
            existing = self.notification_repository.get_by_event_id(command.event_id)
            if existing is not None:
                return existing

        notification = Notification(
            recipient=command.recipient,
            subject=command.subject,
            body=command.body,
            user_id=command.user_id,
            reference_id=command.reference_id,
            event_id=command.event_id,
        )

        try:
            self.sender.send(notification)
            notification.mark_sent(now=self.clock())
        except DeliveryError as error:
            notification.mark_failed(str(error))

        return self.notification_repository.add(notification)
