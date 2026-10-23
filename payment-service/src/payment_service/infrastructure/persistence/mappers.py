from payment_service.domain.entities.payment import Payment, PaymentMethod, PaymentStatus
from payment_service.infrastructure.persistence.models.payment_model import PaymentModel


def to_domain(model: PaymentModel) -> Payment:
    return Payment(
        id=model.id,
        booking_id=model.booking_id,
        user_id=model.user_id,
        amount=model.amount,
        method=PaymentMethod(model.method),
        status=PaymentStatus(model.status),
        failure_reason=model.failure_reason,
        created_at=model.created_at,
        processed_at=model.processed_at,
    )


def to_model(payment: Payment) -> PaymentModel:
    return PaymentModel(
        id=payment.id,
        booking_id=payment.booking_id,
        user_id=payment.user_id,
        amount=payment.amount,
        method=payment.method.value,
        status=payment.status.value,
        failure_reason=payment.failure_reason,
        created_at=payment.created_at,
        processed_at=payment.processed_at,
    )
