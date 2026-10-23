import pytest
from fastapi.testclient import TestClient

from payment_service.main import app
from payment_service.presentation.api import dependencies as deps


@pytest.fixture
def client(repo, create_payment):
    app.dependency_overrides[deps.get_payment_repository] = lambda: repo
    app.dependency_overrides[deps.get_create_payment] = lambda: create_payment
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_crear_y_listar(client, booking):
    created = client.post(
        "/payments", json={"booking_id": str(booking.id), "payment_token": "tok_visa"}
    )
    assert created.status_code == 201
    assert created.json()["status"] == "APPROVED"
    assert len(client.get("/payments", params={"booking_id": str(booking.id)}).json()) == 1


def test_doble_pago_devuelve_409(client, booking):
    body = {"booking_id": str(booking.id), "payment_token": "tok_visa"}
    client.post("/payments", json=body)
    assert client.post("/payments", json=body).status_code == 409
