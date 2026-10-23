"""Entidad Notification. PENDING --mark_sent()--> SENT | --mark_failed()--> FAILED"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from notification_service.domain.exceptions import (
    InvalidNotificationError,
    InvalidNotificationTransitionError,
)
from notification_service.shared.time import utc_now


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"


class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


@dataclass
class Notification:
    recipient: str
    subject: str
    body: str
    channel: NotificationChannel = NotificationChannel.EMAIL
    user_id: uuid.UUID | None = None
    reference_id: uuid.UUID | None = None   # p. ej. id de la reserva
    event_id: uuid.UUID | None = None       # evento que la originó (idempotencia)
    status: NotificationStatus = NotificationStatus.PENDING
    error: str | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)
    sent_at: datetime | None = None

    def __post_init__(self):
        self.recipient = self.recipient.strip().lower()
        if "@" not in self.recipient:
            raise InvalidNotificationError("El destinatario debe ser un email válido")
        if not self.subject.strip():
            raise InvalidNotificationError("El asunto es obligatorio")
        if not self.body.strip():
            raise InvalidNotificationError("El mensaje es obligatorio")

    def mark_sent(self, now: datetime) -> None:
        self._ensure_pending()
        self.status = NotificationStatus.SENT
        self.sent_at = now

    def mark_failed(self, error: str) -> None:
        self._ensure_pending()
        self.status = NotificationStatus.FAILED
        self.error = error

    def _ensure_pending(self) -> None:
        if self.status != NotificationStatus.PENDING:
            raise InvalidNotificationTransitionError("La notificación ya fue procesada")
