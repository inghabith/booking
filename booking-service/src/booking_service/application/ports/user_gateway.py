from abc import ABC, abstractmethod
from uuid import UUID


class UserGateway(ABC):
    @abstractmethod
    def exists(self, user_id: UUID) -> bool: ...
