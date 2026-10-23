"""Entidad Resource: una sala, escritorio o equipo que se puede reservar."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from resources_service.domain.exceptions import InvalidResourceError
from resources_service.shared.time import utc_now


class ResourceType(str, Enum):
    MEETING_ROOM = "MEETING_ROOM"
    AUDITORIUM = "AUDITORIUM"
    DESK = "DESK"
    EQUIPMENT = "EQUIPMENT"


@dataclass
class Resource:
    name: str
    resource_type: ResourceType
    capacity: int
    price_per_hour: Decimal
    location: str = ""
    description: str = ""
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime | None = None

    def __post_init__(self):
        self.name = self.name.strip()
        self.price_per_hour = Decimal(self.price_per_hour)
        if self.updated_at is None:
            self.updated_at = self.created_at

        if not self.name:
            raise InvalidResourceError("El nombre del recurso es obligatorio")
        if self.capacity <= 0:
            raise InvalidResourceError("La capacidad debe ser mayor que 0")
        if self.price_per_hour < 0:
            raise InvalidResourceError("El precio por hora no puede ser negativo")

    # Comportamiento: el estado cambia por métodos con nombre de negocio,
    # no asignando atributos desde afuera.
    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = utc_now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = utc_now()
