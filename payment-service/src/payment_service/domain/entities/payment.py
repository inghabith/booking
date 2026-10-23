"""Entidad Payment. PENDING --approve()--> APPROVED | PENDING --decline()--> DECLINED"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum

from payment_service.domain.exceptions import (
    InvalidPaymentError,
    InvalidPaymentTransitionError,
)
from payment_service.shared.time import utc_now


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"


class PaymentMethod(str, Enum):
    CARD = "CARD"
    PSE = "PSE"


@dataclass
class Payment:
    booking_id: uuid.UUID
    user_id: uuid.UUID
    amount: Decimal
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    failure_reason: str | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)
    processed_at: datetime | None = None

    def __post_init__(self):
        self.amount = Decimal(self.amount)
        if self.amount <= 0:
            raise InvalidPaymentError("El monto del pago debe ser mayor que 0")

    @property
    def is_approved(self) -> bool:
        return self.status == PaymentStatus.APPROVED

    def approve(self, now: datetime) -> None:
        self._ensure_pending()
        self.status = PaymentStatus.APPROVED
        self.processed_at = now

    def decline(self, reason: str, now: datetime) -> None:
        self._ensure_pending()
        self.status = PaymentStatus.DECLINED
        self.failure_reason = reason
        self.processed_at = now

    def _ensure_pending(self) -> None:
        if self.status != PaymentStatus.PENDING:
            raise InvalidPaymentTransitionError(
                f"El pago ya fue procesado (estado: {self.status.value})"
            )
