from resources_service.application.dtos import ResourceFilters
from resources_service.domain.entities.resource import Resource
from resources_service.domain.repositories.resource_repository import ResourceRepository


class ListResources:
    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    def execute(self, filters: ResourceFilters) -> list[Resource]:
        return self.resource_repository.list(
            resource_type=filters.resource_type,
            only_active=filters.only_active,
            min_capacity=filters.min_capacity,
        )
