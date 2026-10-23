from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from payment_service.domain.entities.payment import Payment, PaymentStatus
from payment_service.domain.exceptions import PaymentAlreadyApprovedError
from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.infrastructure.persistence.mappers import to_domain, to_model
from payment_service.infrastructure.persistence.models.payment_model import PaymentModel

UNIQUE_VIOLATION = "23505"


class SQLModelPaymentRepository(PaymentRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, payment: Payment) -> Payment:
        self.session.add(to_model(payment))
        try:
            self.session.flush()
        except IntegrityError as error:
            if getattr(error.orig, "sqlstate", None) == UNIQUE_VIOLATION:
                raise PaymentAlreadyApprovedError(payment.booking_id) from error
            raise
        return payment

    def get_by_id(self, payment_id: UUID) -> Payment | None:
        model = self.session.get(PaymentModel, payment_id)
        return to_domain(model) if model else None

    def get_approved_for_booking(self, booking_id: UUID) -> Payment | None:
        statement = select(PaymentModel).where(
            PaymentModel.booking_id == booking_id,
            PaymentModel.status == PaymentStatus.APPROVED.value,
        )
        model = self.session.exec(statement).first()
        return to_domain(model) if model else None

    def list(self, booking_id: UUID | None = None) -> list[Payment]:
        statement = select(PaymentModel)
        if booking_id is not None:
            statement = statement.where(PaymentModel.booking_id == booking_id)
        statement = statement.order_by(PaymentModel.created_at)
        return [to_domain(model) for model in self.session.exec(statement).all()]
