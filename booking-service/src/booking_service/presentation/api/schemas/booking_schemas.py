import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import AwareDatetime, BaseModel, Field

from booking_service.domain.entities.booking import BookingStatus


class BookingCreateRequest(BaseModel):
    user_id: uuid.UUID
    resource_id: uuid.UUID
    start_at: AwareDatetime = Field(examples=["2026-11-03T14:00:00-05:00"])
    end_at: AwareDatetime = Field(examples=["2026-11-03T16:00:00-05:00"])
    attendees: int = Field(default=1, gt=0)


class BookingResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    resource_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    attendees: int
    total_price: Decimal
    status: BookingStatus
    created_at: datetime
    updated_at: datetime
