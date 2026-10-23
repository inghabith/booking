from uuid import UUID

from sqlmodel import Session, select

from resources_service.domain.entities.resource import Resource, ResourceType
from resources_service.domain.exceptions import ResourceNotFoundError
from resources_service.domain.repositories.resource_repository import ResourceRepository
from resources_service.infrastructure.persistence.mappers import apply_to_model, to_domain
from resources_service.infrastructure.persistence.models.resource_model import ResourceModel


class SQLModelResourceRepository(ResourceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, resource: Resource) -> Resource:
        self.session.add(apply_to_model(resource, ResourceModel(id=resource.id)))
        self.session.flush()
        return resource

    def update(self, resource: Resource) -> Resource:
        model = self.session.get(ResourceModel, resource.id)
        if model is None:
            raise ResourceNotFoundError(resource.id)
        apply_to_model(resource, model)
        self.session.flush()
        return resource

    def get_by_id(self, resource_id: UUID) -> Resource | None:
        model = self.session.get(ResourceModel, resource_id)
        return to_domain(model) if model else None

    def get_by_name(self, name: str) -> Resource | None:
        statement = select(ResourceModel).where(ResourceModel.name == name)
        model = self.session.exec(statement).first()
        return to_domain(model) if model else None

    def list(
        self,
        resource_type: ResourceType | None = None,
        only_active: bool = False,
        min_capacity: int | None = None,
    ) -> list[Resource]:
        statement = select(ResourceModel)
        if resource_type is not None:
            statement = statement.where(ResourceModel.resource_type == resource_type.value)
        if only_active:
            statement = statement.where(ResourceModel.is_active == True)  # noqa: E712
        if min_capacity is not None:
            statement = statement.where(ResourceModel.capacity >= min_capacity)
        statement = statement.order_by(ResourceModel.name)
        return [to_domain(model) for model in self.session.exec(statement).all()]
