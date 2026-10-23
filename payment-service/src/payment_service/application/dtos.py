from dataclasses import dataclass
from uuid import UUID

from payment_service.domain.entities.payment import PaymentMethod


@dataclass(frozen=True)
class CreatePaymentCommand:
    booking_id: UUID
    method: PaymentMethod
    payment_token: str
