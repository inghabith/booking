"""Prueba la garantía de la base: el EXCLUDE impide solapamientos aunque
el caso de uso NO haya detectado el conflicto (p. ej. dos peticiones simultáneas).

Requiere Postgres migrado:
    TEST_DATABASE_URL=postgresql+psycopg://... uv run pytest tests/integration
"""
import os
import uuid
from decimal import Decimal

import pytest
from sqlmodel import Session, create_engine, text

from booking_service.domain.entities.booking import Booking
from booking_service.domain.exceptions import BookingConflictError
from booking_service.domain.value_objects.time_slot import TimeSlot
from booking_service.infrastructure.persistence.repositories.sqlmodel_booking_repository import (
    SQLModelBookingRepository,
)
from tests.conftest import at

DATABASE_URL = os.getenv("TEST_DATABASE_URL", "").replace(
    "postgresql://", "postgresql+psycopg://", 1
)
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="TEST_DATABASE_URL no definida")


@pytest.fixture
def engine():
    return create_engine(DATABASE_URL)


def booking(resource_id, start, end):
    return Booking(
        user_id=uuid.uuid4(),
        resource_id=resource_id,
        slot=TimeSlot(at(start), at(end)),
        total_price=Decimal("0"),
    )


def test_la_base_rechaza_solapamientos(engine):
    resource_id = uuid.uuid4()
    try:
        with Session(engine) as session:
            SQLModelBookingRepository(session).add(booking(resource_id, 10, 12))
            session.commit()

        with Session(engine) as session:
            with pytest.raises(BookingConflictError):
                # Llamamos al repositorio directamente, saltándonos la validación
                # del caso de uso, como pasaría en una carrera.
                SQLModelBookingRepository(session).add(booking(resource_id, 11, 13))
            session.rollback()

        with Session(engine) as session:
            # Contiguas sí se permiten.
            SQLModelBookingRepository(session).add(booking(resource_id, 12, 13))
            session.commit()
    finally:
        with Session(engine) as session:
            session.exec(
                text("DELETE FROM bookings.bookings WHERE resource_id = :rid"),
                params={"rid": resource_id},
            )
            session.commit()


def test_cancelar_libera_el_horario_en_la_base(engine):
    resource_id = uuid.uuid4()
    try:
        with Session(engine) as session:
            repo = SQLModelBookingRepository(session)
            first = repo.add(booking(resource_id, 10, 12))
            first.cancel(now=at(1, day=1))
            repo.update(first)
            repo.add(booking(resource_id, 10, 12))
            session.commit()
    finally:
        with Session(engine) as session:
            session.exec(
                text("DELETE FROM bookings.bookings WHERE resource_id = :rid"),
                params={"rid": resource_id},
            )
            session.commit()
