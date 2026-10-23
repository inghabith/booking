"""Adaptador: implementa el puerto UserRepository con SQLModel."""
from uuid import UUID

from sqlmodel import Session, select

from user_service.domain.entities.user import IdentificationType, User
from user_service.domain.repositories.user_repository import UserRepository
from user_service.infrastructure.persistence.mappers import to_domain, to_model
from user_service.infrastructure.persistence.models.user_model import UserModel


class SQLModelUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        self.session.add(to_model(user))
        # flush envía el INSERT; el commit lo hace get_session al final de la petición.
        self.session.flush()
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        model = self.session.get(UserModel, user_id)
        return to_domain(model) if model else None

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email.lower())
        model = self.session.exec(statement).first()
        return to_domain(model) if model else None

    def get_by_identification(
        self, identification_type: IdentificationType, identification_number: str
    ) -> User | None:
        statement = select(UserModel).where(
            UserModel.identification_type == identification_type.value,
            UserModel.identification_number == identification_number,
        )
        model = self.session.exec(statement).first()
        return to_domain(model) if model else None

    def list(self, limit: int = 50, offset: int = 0) -> list[User]:
        statement = (
            select(UserModel).order_by(UserModel.created_at).offset(offset).limit(limit)
        )
        return [to_domain(model) for model in self.session.exec(statement).all()]
