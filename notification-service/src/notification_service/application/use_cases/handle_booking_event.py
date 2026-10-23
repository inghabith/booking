from uuid import UUID

from notification_service.application import templates
from notification_service.application.dtos import IntegrationEvent, SendNotificationCommand
from notification_service.application.ports.user_directory import UserDirectory
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.domain.entities.notification import Notification
from notification_service.domain.exceptions import NotFoundError


class RecipientNotFoundError(NotFoundError):
    def __init__(self, user_id):
        super().__init__(f"El usuario {user_id} no existe en user-service")


class HandleBookingEvent:
    """Reacciona a eventos de booking-service. Reutiliza SendNotification."""

    def __init__(self, user_directory: UserDirectory, send_notification: SendNotification):
        self.user_directory = user_directory
        self.send_notification = send_notification

    def execute(self, event: IntegrationEvent) -> Notification:
        user_id = UUID(event.data["user_id"])
        contact = self.user_directory.get_contact(user_id)
        if contact is None:
            raise RecipientNotFoundError(user_id)

        subject, body = templates.render(event, contact)

        return self.send_notification.execute(
            SendNotificationCommand(
                recipient=contact.email,
                subject=subject,
                body=body,
                user_id=user_id,
                reference_id=UUID(event.data["booking_id"]),
                event_id=event.event_id,
            )
        )
