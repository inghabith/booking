from notification_service.domain.entities.notification import (
    Notification,
    NotificationChannel,
    NotificationStatus,
)
from notification_service.infrastructure.persistence.models.notification_model import (
    NotificationModel,
)


def to_domain(model: NotificationModel) -> Notification:
    return Notification(
        id=model.id,
        recipient=model.recipient,
        channel=NotificationChannel(model.channel),
        subject=model.subject,
        body=model.body,
        user_id=model.user_id,
        reference_id=model.reference_id,
        event_id=model.event_id,
        status=NotificationStatus(model.status),
        error=model.error,
        created_at=model.created_at,
        sent_at=model.sent_at,
    )


def to_model(notification: Notification) -> NotificationModel:
    return NotificationModel(
        id=notification.id,
        recipient=notification.recipient,
        channel=notification.channel.value,
        subject=notification.subject,
        body=notification.body,
        user_id=notification.user_id,
        reference_id=notification.reference_id,
        event_id=notification.event_id,
        status=notification.status.value,
        error=notification.error,
        created_at=notification.created_at,
        sent_at=notification.sent_at,
    )
