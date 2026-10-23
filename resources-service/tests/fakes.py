from resources_service.domain.repositories.resource_repository import ResourceRepository


class InMemoryResourceRepository(ResourceRepository):
    def __init__(self):
        self.resources = {}

    def add(self, resource):
        self.resources[resource.id] = resource
        return resource

    def update(self, resource):
        self.resources[resource.id] = resource
        return resource

    def get_by_id(self, resource_id):
        return self.resources.get(resource_id)

    def get_by_name(self, name):
        return next((r for r in self.resources.values() if r.name == name), None)

    def list(self, resource_type=None, only_active=False, min_capacity=None):
        result = list(self.resources.values())
        if resource_type:
            result = [r for r in result if r.resource_type == resource_type]
        if only_active:
            result = [r for r in result if r.is_active]
        if min_capacity:
            result = [r for r in result if r.capacity >= min_capacity]
        return result
