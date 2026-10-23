from uuid import UUID

from notification_service.domain.entities.notification import Notification
from notification_service.domain.exceptions import NotificationNotFoundError
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)


class GetNotification:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(self, notification_id: UUID) -> Notification:
        notification = self.notification_repository.get_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError(notification_id)
        return notification
