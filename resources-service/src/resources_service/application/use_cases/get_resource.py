from uuid import UUID

from resources_service.domain.entities.resource import Resource
from resources_service.domain.exceptions import ResourceNotFoundError
from resources_service.domain.repositories.resource_repository import ResourceRepository


class GetResource:
    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    def execute(self, resource_id: UUID) -> Resource:
        resource = self.resource_repository.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotFoundError(resource_id)
        return resource
