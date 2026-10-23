import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from resources_service.domain.entities.resource import ResourceType


class ResourceCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    resource_type: ResourceType
    capacity: int = Field(gt=0)
    price_per_hour: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    location: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=1000)


class ResourceResponse(BaseModel):
    id: uuid.UUID
    name: str
    resource_type: ResourceType
    capacity: int
    price_per_hour: Decimal
    location: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
