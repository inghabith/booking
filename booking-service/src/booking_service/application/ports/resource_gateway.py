"""Puerto hacia resources-service. booking no conoce su base ni sus modelos."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ResourceSnapshot:
    """Lo mínimo que booking necesita saber de un recurso (contrato explícito)."""

    id: UUID
    name: str
    capacity: int
    price_per_hour: Decimal
    is_active: bool


class ResourceGateway(ABC):
    @abstractmethod
    def get(self, resource_id: UUID) -> ResourceSnapshot | None: ...
