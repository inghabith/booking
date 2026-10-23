"""Contrato HTTP (Pydantic). Puede cambiar sin tocar el dominio."""
import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field

from user_service.domain.entities.user import IdentificationType


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    identification_type: IdentificationType
    identification_number: str = Field(min_length=1, max_length=30)
    birthday_date: date


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    identification_type: IdentificationType
    identification_number: str
    birthday_date: date
    created_at: datetime
