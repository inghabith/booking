from uuid import UUID

from notification_service.domain.entities.notification import Notification
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)


class ListNotifications:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def execute(
        self, user_id: UUID | None = None, reference_id: UUID | None = None
    ) -> list[Notification]:
        return self.notification_repository.list(user_id=user_id, reference_id=reference_id)
