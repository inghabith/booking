from resources_service.domain.entities.resource import Resource, ResourceType
from resources_service.infrastructure.persistence.models.resource_model import ResourceModel


def to_domain(model: ResourceModel) -> Resource:
    return Resource(
        id=model.id,
        name=model.name,
        resource_type=ResourceType(model.resource_type),
        capacity=model.capacity,
        price_per_hour=model.price_per_hour,
        location=model.location,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def apply_to_model(resource: Resource, model: ResourceModel) -> ResourceModel:
    model.name = resource.name
    model.resource_type = resource.resource_type.value
    model.capacity = resource.capacity
    model.price_per_hour = resource.price_per_hour
    model.location = resource.location
    model.description = resource.description
    model.is_active = resource.is_active
    model.created_at = resource.created_at
    model.updated_at = resource.updated_at
    return model
