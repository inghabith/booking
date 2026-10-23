"""Puerto hacia user-service: los eventos traen user_id, no el email."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserContact:
    name: str
    email: str


class UserDirectory(ABC):
    @abstractmethod
    def get_contact(self, user_id: UUID) -> UserContact | None: ...
