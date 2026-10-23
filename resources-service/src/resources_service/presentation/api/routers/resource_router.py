from uuid import UUID

from fastapi import APIRouter, Depends, Query

from resources_service.application.dtos import CreateResourceCommand, ResourceFilters
from resources_service.application.use_cases.change_resource_status import (
    ChangeResourceStatus,
)
from resources_service.application.use_cases.create_resource import CreateResource
from resources_service.application.use_cases.get_resource import GetResource
from resources_service.application.use_cases.list_resources import ListResources
from resources_service.domain.entities.resource import Resource, ResourceType
from resources_service.presentation.api.dependencies import (
    get_change_resource_status,
    get_create_resource,
    get_get_resource,
    get_list_resources,
)
from resources_service.presentation.api.schemas.resource_schemas import (
    ResourceCreateRequest,
    ResourceResponse,
)

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", status_code=201)
def create_resource(
    payload: ResourceCreateRequest,
    use_case: CreateResource = Depends(get_create_resource),
) -> ResourceResponse:
    command = CreateResourceCommand(**payload.model_dump())
    return to_response(use_case.execute(command))


@router.get("")
def list_resources(
    resource_type: ResourceType | None = None,
    only_active: bool = False,
    min_capacity: int | None = Query(None, gt=0),
    use_case: ListResources = Depends(get_list_resources),
) -> list[ResourceResponse]:
    filters = ResourceFilters(resource_type, only_active, min_capacity)
    return [to_response(resource) for resource in use_case.execute(filters)]


@router.get("/{resource_id}")
def get_resource(
    resource_id: UUID, use_case: GetResource = Depends(get_get_resource)
) -> ResourceResponse:
    return to_response(use_case.execute(resource_id))


@router.post("/{resource_id}/activate")
def activate_resource(
    resource_id: UUID,
    use_case: ChangeResourceStatus = Depends(get_change_resource_status),
) -> ResourceResponse:
    return to_response(use_case.execute(resource_id, active=True))


@router.post("/{resource_id}/deactivate")
def deactivate_resource(
    resource_id: UUID,
    use_case: ChangeResourceStatus = Depends(get_change_resource_status),
) -> ResourceResponse:
    return to_response(use_case.execute(resource_id, active=False))


def to_response(resource: Resource) -> ResourceResponse:
    return ResourceResponse(
        id=resource.id,
        name=resource.name,
        resource_type=resource.resource_type,
        capacity=resource.capacity,
        price_per_hour=resource.price_per_hour,
        location=resource.location,
        description=resource.description,
        is_active=resource.is_active,
        created_at=resource.created_at,
        updated_at=resource.updated_at,
    )
