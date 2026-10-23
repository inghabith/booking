import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from notification_service.shared.config import DB_SCHEMA
from notification_service.shared.time import utc_now


class NotificationModel(SQLModel, table=True):
    __tablename__ = "notifications"
    __table_args__ = {"schema": DB_SCHEMA}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    recipient: str = Field(max_length=254)
    channel: str = Field(max_length=20)
    subject: str = Field(max_length=200)
    body: str = Field(max_length=2000)
    user_id: uuid.UUID | None = Field(default=None, index=True)
    reference_id: uuid.UUID | None = Field(default=None, index=True)
    # unique: el mismo evento nunca genera dos notificaciones.
    event_id: uuid.UUID | None = Field(default=None, unique=True)
    status: str = Field(max_length=20)
    error: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
    sent_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))
