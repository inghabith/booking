from dataclasses import dataclass
from decimal import Decimal

from resources_service.domain.entities.resource import ResourceType


@dataclass(frozen=True)
class CreateResourceCommand:
    name: str
    resource_type: ResourceType
    capacity: int
    price_per_hour: Decimal
    location: str = ""
    description: str = ""


@dataclass(frozen=True)
class ResourceFilters:
    resource_type: ResourceType | None = None
    only_active: bool = False
    min_capacity: int | None = None
