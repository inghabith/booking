import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from payment_service.domain.entities.payment import PaymentMethod, PaymentStatus


class PaymentCreateRequest(BaseModel):
    booking_id: uuid.UUID
    method: PaymentMethod = PaymentMethod.CARD
    payment_token: str = Field(min_length=1, examples=["tok_visa", "tok_declined"])


class PaymentResponse(BaseModel):
    id: uuid.UUID
    booking_id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    method: PaymentMethod
    status: PaymentStatus
    failure_reason: str | None
    created_at: datetime
    processed_at: datetime | None
