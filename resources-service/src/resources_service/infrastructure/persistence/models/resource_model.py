import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from resources_service.shared.config import DB_SCHEMA
from resources_service.shared.time import utc_now


class ResourceModel(SQLModel, table=True):
    __tablename__ = "resources"
    __table_args__ = {"schema": DB_SCHEMA}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=120, unique=True)
    resource_type: str = Field(max_length=30, index=True)
    capacity: int
    price_per_hour: Decimal = Field(max_digits=12, decimal_places=2)
    location: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=1000)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=utc_now, sa_type=DateTime(timezone=True))
