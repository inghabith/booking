from abc import ABC, abstractmethod
from uuid import UUID

from resources_service.domain.entities.resource import Resource, ResourceType


class ResourceRepository(ABC):
    @abstractmethod
    def add(self, resource: Resource) -> Resource: ...

    @abstractmethod
    def update(self, resource: Resource) -> Resource: ...

    @abstractmethod
    def get_by_id(self, resource_id: UUID) -> Resource | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Resource | None: ...

    @abstractmethod
    def list(
        self,
        resource_type: ResourceType | None = None,
        only_active: bool = False,
        min_capacity: int | None = None,
    ) -> list[Resource]: ...
