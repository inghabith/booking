from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class SendNotificationCommand:
    recipient: str
    subject: str
    body: str
    user_id: UUID | None = None
    reference_id: UUID | None = None
    event_id: UUID | None = None


@dataclass(frozen=True)
class IntegrationEvent:
    """Mensaje recibido de otro servicio: {"event", "event_id", "occurred_at", "data"}."""

    name: str
    event_id: UUID
    data: dict[str, Any] = field(default_factory=dict)
