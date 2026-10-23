from abc import ABC, abstractmethod
from uuid import UUID

from payment_service.domain.entities.payment import Payment


class PaymentRepository(ABC):
    @abstractmethod
    def add(self, payment: Payment) -> Payment:
        """Debe lanzar PaymentAlreadyApprovedError si la base detecta un 2.º aprobado."""

    @abstractmethod
    def get_by_id(self, payment_id: UUID) -> Payment | None: ...

    @abstractmethod
    def get_approved_for_booking(self, booking_id: UUID) -> Payment | None: ...

    @abstractmethod
    def list(self, booking_id: UUID | None = None) -> list[Payment]: ...
