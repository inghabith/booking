from resources_service.application.dtos import CreateResourceCommand
from resources_service.domain.entities.resource import Resource
from resources_service.domain.exceptions import ResourceAlreadyExistsError
from resources_service.domain.repositories.resource_repository import ResourceRepository


class CreateResource:
    def __init__(self, resource_repository: ResourceRepository):
        self.resource_repository = resource_repository

    def execute(self, command: CreateResourceCommand) -> Resource:
        resource = Resource(
            name=command.name,
            resource_type=command.resource_type,
            capacity=command.capacity,
            price_per_hour=command.price_per_hour,
            location=command.location,
            description=command.description,
        )

        if self.resource_repository.get_by_name(resource.name):
            raise ResourceAlreadyExistsError(f"Ya existe un recurso llamado {resource.name}")

        return self.resource_repository.add(resource)
