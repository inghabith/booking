from abc import ABC, abstractmethod
from uuid import UUID

from notification_service.domain.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def add(self, notification: Notification) -> Notification: ...

    @abstractmethod
    def get_by_id(self, notification_id: UUID) -> Notification | None: ...

    @abstractmethod
    def get_by_event_id(self, event_id: UUID) -> Notification | None: ...

    @abstractmethod
    def list(
        self, user_id: UUID | None = None, reference_id: UUID | None = None
    ) -> list[Notification]: ...
