"""Adaptador REST hacia user-service (contrato: GET /users/{id})."""
from uuid import UUID

import httpx

from notification_service.application.exceptions import ExternalServiceError
from notification_service.application.ports.user_directory import UserContact, UserDirectory


class HttpUserDirectory(UserDirectory):
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    def get_contact(self, user_id: UUID) -> UserContact | None:
        try:
            response = httpx.get(f"{self.base_url}/users/{user_id}", timeout=self.timeout)
        except httpx.HTTPError as error:
            raise ExternalServiceError("user-service no está disponible") from error

        if response.status_code == 404:
            return None
        if response.is_error:
            raise ExternalServiceError(f"user-service respondió {response.status_code}")

        data = response.json()
        return UserContact(name=data["name"], email=data["email"])
