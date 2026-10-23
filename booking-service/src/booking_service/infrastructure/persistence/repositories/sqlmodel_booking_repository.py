from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from booking_service.domain.entities.booking import Booking, BookingStatus
from booking_service.domain.exceptions import BookingConflictError, BookingNotFoundError
from booking_service.domain.repositories.booking_repository import BookingRepository
from booking_service.domain.value_objects.time_slot import TimeSlot
from booking_service.infrastructure.persistence.mappers import apply_to_model, to_domain
from booking_service.infrastructure.persistence.models.booking_model import BookingModel

# SQLSTATE de Postgres para "exclusion_violation" (la constraint anti-solapamiento).
EXCLUSION_VIOLATION = "23P01"


class SQLModelBookingRepository(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, booking: Booking) -> Booking:
        self.session.add(apply_to_model(booking, BookingModel(id=booking.id)))
        self._flush(booking)
        return booking

    def update(self, booking: Booking) -> Booking:
        model = self.session.get(BookingModel, booking.id)
        if model is None:
            raise BookingNotFoundError(booking.id)
        apply_to_model(booking, model)
        self._flush(booking)
        return booking

    def get_by_id(self, booking_id: UUID) -> Booking | None:
        model = self.session.get(BookingModel, booking_id)
        return to_domain(model) if model else None

    def find_active_overlapping(self, resource_id: UUID, slot: TimeSlot) -> list[Booking]:
        statement = select(BookingModel).where(
            BookingModel.resource_id == resource_id,
            BookingModel.status != BookingStatus.CANCELLED.value,
            BookingModel.start_at < slot.end_at,
            BookingModel.end_at > slot.start_at,
        )
        return [to_domain(model) for model in self.session.exec(statement).all()]

    def list(
        self,
        user_id: UUID | None = None,
        resource_id: UUID | None = None,
        status: BookingStatus | None = None,
    ) -> list[Booking]:
        statement = select(BookingModel)
        if user_id is not None:
            statement = statement.where(BookingModel.user_id == user_id)
        if resource_id is not None:
            statement = statement.where(BookingModel.resource_id == resource_id)
        if status is not None:
            statement = statement.where(BookingModel.status == status.value)
        statement = statement.order_by(BookingModel.start_at)
        return [to_domain(model) for model in self.session.exec(statement).all()]

    def _flush(self, booking: Booking) -> None:
        try:
            self.session.flush()
        except IntegrityError as error:
            # Traducimos el error técnico de la base al error de dominio.
            if getattr(error.orig, "sqlstate", None) == EXCLUSION_VIOLATION:
                raise BookingConflictError(booking.resource_id) from error
            raise
