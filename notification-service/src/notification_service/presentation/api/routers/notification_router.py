from uuid import UUID

from fastapi import APIRouter, Depends

from notification_service.application.dtos import SendNotificationCommand
from notification_service.application.use_cases.get_notification import GetNotification
from notification_service.application.use_cases.list_notifications import ListNotifications
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.domain.entities.notification import Notification
from notification_service.presentation.api.dependencies import (
    get_get_notification,
    get_list_notifications,
    get_send_notification,
)
from notification_service.presentation.api.schemas.notification_schemas import (
    NotificationCreateRequest,
    NotificationResponse,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("", status_code=201)
def send_notification(
    payload: NotificationCreateRequest,
    use_case: SendNotification = Depends(get_send_notification),
) -> NotificationResponse:
    command = SendNotificationCommand(**payload.model_dump())
    return to_response(use_case.execute(command))


@router.get("")
def list_notifications(
    user_id: UUID | None = None,
    reference_id: UUID | None = None,
    use_case: ListNotifications = Depends(get_list_notifications),
) -> list[NotificationResponse]:
    return [to_response(n) for n in use_case.execute(user_id, reference_id)]


@router.get("/{notification_id}")
def get_notification(
    notification_id: UUID, use_case: GetNotification = Depends(get_get_notification)
) -> NotificationResponse:
    return to_response(use_case.execute(notification_id))


def to_response(notification: Notification) -> NotificationResponse:
    return NotificationResponse(
        id=notification.id,
        recipient=notification.recipient,
        channel=notification.channel,
        subject=notification.subject,
        body=notification.body,
        user_id=notification.user_id,
        reference_id=notification.reference_id,
        event_id=notification.event_id,
        status=notification.status,
        error=notification.error,
        created_at=notification.created_at,
        sent_at=notification.sent_at,
    )
