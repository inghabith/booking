"""DTOs de entrada de los casos de uso. Desacoplan HTTP del dominio."""
from dataclasses import dataclass
from datetime import date

from user_service.domain.entities.user import IdentificationType


@dataclass(frozen=True)
class CreateUserCommand:
    name: str
    email: str
    identification_type: IdentificationType
    identification_number: str
    birthday_date: date
