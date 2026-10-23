from abc import ABC, abstractmethod

from notification_service.domain.entities.notification import Notification


class NotificationSender(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Entrega el mensaje o lanza DeliveryError."""
