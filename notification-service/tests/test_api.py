import pytest
from fastapi.testclient import TestClient

from notification_service.main import app
from notification_service.presentation.api import dependencies as deps
from tests.fakes import InMemoryNotificationRepository, SpySender


@pytest.fixture
def client():
    repo = InMemoryNotificationRepository()
    app.dependency_overrides[deps.get_notification_repository] = lambda: repo
    app.dependency_overrides[deps.get_sender] = lambda: SpySender()
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_enviar_y_consultar(client):
    created = client.post(
        "/notifications",
        json={"recipient": "ana@mail.com", "subject": "Hola", "body": "Prueba"},
    )
    assert created.status_code == 201
    assert created.json()["status"] == "SENT"
    assert client.get(f"/notifications/{created.json()['id']}").status_code == 200


def test_email_invalido_devuelve_422(client):
    response = client.post(
        "/notifications", json={"recipient": "no-es-email", "subject": "a", "body": "b"}
    )
    assert response.status_code == 422
