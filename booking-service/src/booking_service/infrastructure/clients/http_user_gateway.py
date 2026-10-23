"""Adaptador REST hacia user-service (contrato: GET /users/{id})."""
from uuid import UUID

import httpx

from booking_service.application.exceptions import ExternalServiceError
from booking_service.application.ports.user_gateway import UserGateway


class HttpUserGateway(UserGateway):
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    def exists(self, user_id: UUID) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/users/{user_id}", timeout=self.timeout)
        except httpx.HTTPError as error:
            raise ExternalServiceError("user-service no está disponible") from error

        if response.status_code == 404:
            return False
        if response.is_error:
            raise ExternalServiceError(f"user-service respondió {response.status_code}")
        return True
