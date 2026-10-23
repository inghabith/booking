import pytest
from fastapi.testclient import TestClient

from tests.fakes import InMemoryUserRepository
from user_service.main import app
from user_service.presentation.api.dependencies import get_user_repository


@pytest.fixture
def client():
    repo = InMemoryUserRepository()
    app.dependency_overrides[get_user_repository] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


PAYLOAD = {
    "name": "Ana",
    "email": "ana@mail.com",
    "identification_type": "CC",
    "identification_number": "1001",
    "birthday_date": "1999-05-01",
}


def test_crear_y_consultar(client):
    created = client.post("/users", json=PAYLOAD)
    assert created.status_code == 201
    user_id = created.json()["id"]
    assert client.get(f"/users/{user_id}").json()["email"] == "ana@mail.com"


def test_duplicado_devuelve_409(client):
    client.post("/users", json=PAYLOAD)
    assert client.post("/users", json=PAYLOAD).status_code == 409


def test_no_existe_devuelve_404(client):
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
