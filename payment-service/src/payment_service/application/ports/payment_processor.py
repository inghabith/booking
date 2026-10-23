"""Puerto hacia la pasarela de pagos (hoy simulada; mañana Wompi, Stripe, etc.)."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from payment_service.domain.entities.payment import PaymentMethod


@dataclass(frozen=True)
class ChargeResult:
    approved: bool
    reason: str | None = None


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: Decimal, method: PaymentMethod, payment_token: str) -> ChargeResult: ...
