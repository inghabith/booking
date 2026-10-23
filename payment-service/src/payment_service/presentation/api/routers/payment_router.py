from uuid import UUID

from fastapi import APIRouter, Depends

from payment_service.application.dtos import CreatePaymentCommand
from payment_service.application.use_cases.create_payment import CreatePayment
from payment_service.application.use_cases.get_payment import GetPayment
from payment_service.application.use_cases.list_payments import ListPayments
from payment_service.domain.entities.payment import Payment
from payment_service.presentation.api.dependencies import (
    get_create_payment,
    get_get_payment,
    get_list_payments,
)
from payment_service.presentation.api.schemas.payment_schemas import (
    PaymentCreateRequest,
    PaymentResponse,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", status_code=201)
def create_payment(
    payload: PaymentCreateRequest, use_case: CreatePayment = Depends(get_create_payment)
) -> PaymentResponse:
    command = CreatePaymentCommand(**payload.model_dump())
    return to_response(use_case.execute(command))


@router.get("")
def list_payments(
    booking_id: UUID | None = None, use_case: ListPayments = Depends(get_list_payments)
) -> list[PaymentResponse]:
    return [to_response(payment) for payment in use_case.execute(booking_id)]


@router.get("/{payment_id}")
def get_payment(
    payment_id: UUID, use_case: GetPayment = Depends(get_get_payment)
) -> PaymentResponse:
    return to_response(use_case.execute(payment_id))


def to_response(payment: Payment) -> PaymentResponse:
    return PaymentResponse(
        id=payment.id,
        booking_id=payment.booking_id,
        user_id=payment.user_id,
        amount=payment.amount,
        method=payment.method,
        status=payment.status,
        failure_reason=payment.failure_reason,
        created_at=payment.created_at,
        processed_at=payment.processed_at,
    )
