"""Traducción entidad <-> modelo. El dominio nunca ve un UserModel."""
from user_service.domain.entities.user import IdentificationType, User
from user_service.infrastructure.persistence.models.user_model import UserModel


def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
        email=model.email,
        identification_type=IdentificationType(model.identification_type),
        identification_number=model.identification_number,
        birthday_date=model.birthday_date,
        created_at=model.created_at,
    )


def to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        name=user.name,
        email=user.email,
        identification_type=user.identification_type.value,
        identification_number=user.identification_number,
        birthday_date=user.birthday_date,
        created_at=user.created_at,
    )
