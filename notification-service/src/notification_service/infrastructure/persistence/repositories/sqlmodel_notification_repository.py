from uuid import UUID

from sqlmodel import Session, select

from notification_service.domain.entities.notification import Notification
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)
from notification_service.infrastructure.persistence.mappers import to_domain, to_model
from notification_service.infrastructure.persistence.models.notification_model import (
    NotificationModel,
)


class SQLModelNotificationRepository(NotificationRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, notification: Notification) -> Notification:
        self.session.add(to_model(notification))
        self.session.flush()
        return notification

    def get_by_id(self, notification_id: UUID) -> Notification | None:
        model = self.session.get(NotificationModel, notification_id)
        return to_domain(model) if model else None

    def get_by_event_id(self, event_id: UUID) -> Notification | None:
        statement = select(NotificationModel).where(NotificationModel.event_id == event_id)
        model = self.session.exec(statement).first()
        return to_domain(model) if model else None

    def list(
        self, user_id: UUID | None = None, reference_id: UUID | None = None
    ) -> list[Notification]:
        statement = select(NotificationModel)
        if user_id is not None:
            statement = statement.where(NotificationModel.user_id == user_id)
        if reference_id is not None:
            statement = statement.where(NotificationModel.reference_id == reference_id)
        statement = statement.order_by(NotificationModel.created_at)
        return [to_domain(model) for model in self.session.exec(statement).all()]
