import pytest
from fastapi.testclient import TestClient

from booking_service.application.use_cases.cancel_booking import CancelBooking
from booking_service.application.use_cases.create_booking import CreateBooking
from booking_service.main import app
from booking_service.presentation.api import dependencies as deps


@pytest.fixture
def client(repo, resources, users, publisher, clock):
    app.dependency_overrides[deps.get_booking_repository] = lambda: repo
    app.dependency_overrides[deps.get_event_publisher] = lambda: publisher
    app.dependency_overrides[deps.get_create_booking] = lambda: CreateBooking(
        repo, resources, users, clock=clock
    )
    app.dependency_overrides[deps.get_cancel_booking] = lambda: CancelBooking(
        repo, publisher, clock=clock
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def payload(user_id, room, start="10:00", end="12:00"):
    return {
        "user_id": str(user_id),
        "resource_id": str(room.id),
        "start_at": f"2026-11-03T{start}:00Z",
        "end_at": f"2026-11-03T{end}:00Z",
        "attendees": 2,
    }


def test_flujo_crear_confirmar_cancelar(client, user_id, room, publisher):
    created = client.post("/bookings", json=payload(user_id, room))
    assert created.status_code == 201
    body = created.json()
    assert body["total_price"] == "100000.00"

    confirmed = client.post(f"/bookings/{body['id']}/confirm")
    assert confirmed.json()["status"] == "CONFIRMED"
    assert client.post(f"/bookings/{body['id']}/confirm").status_code == 409

    assert client.post(f"/bookings/{body['id']}/cancel").json()["status"] == "CANCELLED"
    assert [e.name for e in publisher.events] == ["booking.confirmed", "booking.cancelled"]


def test_solapamiento_devuelve_409(client, user_id, room):
    client.post("/bookings", json=payload(user_id, room))
    response = client.post("/bookings", json=payload(user_id, room, "11:00", "13:00"))
    assert response.status_code == 409


def test_fecha_sin_zona_horaria_devuelve_422(client, user_id, room):
    data = payload(user_id, room)
    data["start_at"] = "2026-11-03T10:00:00"
    assert client.post("/bookings", json=data).status_code == 422


def test_filtrar_por_recurso(client, user_id, room):
    client.post("/bookings", json=payload(user_id, room))
    listed = client.get("/bookings", params={"resource_id": str(room.id)}).json()
    assert len(listed) == 1
