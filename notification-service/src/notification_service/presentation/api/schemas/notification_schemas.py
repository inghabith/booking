import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from notification_service.domain.entities.notification import (
    NotificationChannel,
    NotificationStatus,
)


class NotificationCreateRequest(BaseModel):
    recipient: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=2000)
    user_id: uuid.UUID | None = None
    reference_id: uuid.UUID | None = None


class NotificationResponse(BaseModel):
    id: uuid.UUID
    recipient: str
    channel: NotificationChannel
    subject: str
    body: str
    user_id: uuid.UUID | None
    reference_id: uuid.UUID | None
    event_id: uuid.UUID | None
    status: NotificationStatus
    error: str | None
    created_at: datetime
    sent_at: datetime | None
