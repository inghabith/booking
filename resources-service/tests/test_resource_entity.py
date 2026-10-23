from decimal import Decimal

import pytest

from resources_service.domain.entities.resource import Resource, ResourceType
from resources_service.domain.exceptions import InvalidResourceError


def make(**overrides):
    data = dict(
        name="Sala Caribe",
        resource_type=ResourceType.MEETING_ROOM,
        capacity=8,
        price_per_hour=Decimal("50000"),
    )
    data.update(overrides)
    return Resource(**data)


def test_capacidad_cero_falla():
    with pytest.raises(InvalidResourceError):
        make(capacity=0)


def test_precio_negativo_falla():
    with pytest.raises(InvalidResourceError):
        make(price_per_hour=Decimal("-1"))


def test_desactivar():
    resource = make()
    resource.deactivate()
    assert resource.is_active is False
