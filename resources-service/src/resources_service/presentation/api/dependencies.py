"""Composition root del servicio."""
from fastapi import Depends

from resources_service.application.use_cases.change_resource_status import (
    ChangeResourceStatus,
)
from resources_service.application.use_cases.create_resource import CreateResource
from resources_service.application.use_cases.get_resource import GetResource
from resources_service.application.use_cases.list_resources import ListResources
from resources_service.domain.repositories.resource_repository import ResourceRepository
from resources_service.infrastructure.database.session import get_session
from resources_service.infrastructure.persistence.repositories.sqlmodel_resource_repository import (
    SQLModelResourceRepository,
)


def get_resource_repository(
    session=Depends(get_session, scope="function"),
) -> ResourceRepository:
    return SQLModelResourceRepository(session)


def get_create_resource(repository=Depends(get_resource_repository)) -> CreateResource:
    return CreateResource(repository)


def get_get_resource(repository=Depends(get_resource_repository)) -> GetResource:
    return GetResource(repository)


def get_list_resources(repository=Depends(get_resource_repository)) -> ListResources:
    return ListResources(repository)


def get_change_resource_status(
    repository=Depends(get_resource_repository),
) -> ChangeResourceStatus:
    return ChangeResourceStatus(repository)
