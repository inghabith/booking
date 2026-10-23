"""Adaptador REST hacia resources-service (contrato: GET /resources/{id})."""
from decimal import Decimal
from uuid import UUID

import httpx

from booking_service.application.exceptions import ExternalServiceError
from booking_service.application.ports.resource_gateway import ResourceGateway, ResourceSnapshot


class HttpResourceGateway(ResourceGateway):
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, resource_id: UUID) -> ResourceSnapshot | None:
        try:
            response = httpx.get(f"{self.base_url}/resources/{resource_id}", timeout=self.timeout)
        except httpx.HTTPError as error:
            raise ExternalServiceError("resources-service no está disponible") from error

        if response.status_code == 404:
            return None
        if response.is_error:
            raise ExternalServiceError(f"resources-service respondió {response.status_code}")

        data = response.json()
        return ResourceSnapshot(
            id=UUID(data["id"]),
            name=data["name"],
            capacity=int(data["capacity"]),
            price_per_hour=Decimal(str(data["price_per_hour"])),
            is_active=bool(data["is_active"]),
        )
