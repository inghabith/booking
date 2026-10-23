import pytest
from fastapi.testclient import TestClient

from resources_service.main import app
from resources_service.presentation.api.dependencies import get_resource_repository
from tests.fakes import InMemoryResourceRepository


@pytest.fixture
def client():
    repo = InMemoryResourceRepository()
    app.dependency_overrides[get_resource_repository] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


PAYLOAD = {
    "name": "Sala Caribe",
    "resource_type": "MEETING_ROOM",
    "capacity": 8,
    "price_per_hour": "50000.00",
}


def test_crear_desactivar_y_filtrar(client):
    created = client.post("/resources", json=PAYLOAD).json()
    client.post(f"/resources/{created['id']}/deactivate")

    assert client.get(f"/resources/{created['id']}").json()["is_active"] is False
    assert client.get("/resources", params={"only_active": True}).json() == []


def test_nombre_duplicado_devuelve_409(client):
    client.post("/resources", json=PAYLOAD)
    assert client.post("/resources", json=PAYLOAD).status_code == 409


def test_capacidad_invalida_devuelve_422(client):
    assert client.post("/resources", json={**PAYLOAD, "capacity": 0}).status_code == 422
