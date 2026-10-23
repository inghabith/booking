"""Entidad User: Python puro. No conoce SQLModel, FastAPI ni la base de datos."""
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum

from user_service.domain.exceptions import InvalidUserError
from user_service.shared.time import utc_now


class IdentificationType(str, Enum):
    CC = "CC"
    CE = "CE"
    TI = "TI"
    PASSPORT = "PASSPORT"


@dataclass
class User:
    name: str
    email: str
    identification_type: IdentificationType
    identification_number: str
    birthday_date: date
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self):
        # Invariantes: un User inválido no puede existir en memoria.
        self.name = self.name.strip()
        self.email = self.email.strip().lower()
        self.identification_number = self.identification_number.strip()

        if not self.name:
            raise InvalidUserError("El nombre es obligatorio")
        if "@" not in self.email:
            raise InvalidUserError("El email no es válido")
        if not self.identification_number:
            raise InvalidUserError("El número de identificación es obligatorio")
        if self.birthday_date >= date.today():
            raise InvalidUserError("La fecha de nacimiento debe ser una fecha pasada")
