"""Puerto de persistencia: qué necesita el negocio, no cómo se guarda."""
from abc import ABC, abstractmethod
from uuid import UUID

from user_service.domain.entities.user import IdentificationType, User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: ...

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_identification(
        self, identification_type: IdentificationType, identification_number: str
    ) -> User | None: ...

    @abstractmethod
    def list(self, limit: int = 50, offset: int = 0) -> list[User]: ...
