"""Adaptador REST hacia booking-service.

Contrato: GET /bookings/{id}  y  POST /bookings/{id}/confirm
"""
from decimal import Decimal
from uuid import UUID

import httpx

from payment_service.application.exceptions import ExternalServiceError
from payment_service.application.ports.booking_gateway import BookingGateway, BookingSnapshot


class HttpBookingGateway(BookingGateway):
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, booking_id: UUID) -> BookingSnapshot | None:
        response = self._request("GET", f"/bookings/{booking_id}")
        if response.status_code == 404:
            return None
        self._raise_for_error(response)
        data = response.json()
        return BookingSnapshot(
            id=UUID(data["id"]),
            user_id=UUID(data["user_id"]),
            status=data["status"],
            total_price=Decimal(str(data["total_price"])),
        )

    def confirm(self, booking_id: UUID) -> None:
        response = self._request("POST", f"/bookings/{booking_id}/confirm")
        self._raise_for_error(response)

    def _request(self, method: str, path: str) -> httpx.Response:
        try:
            return httpx.request(method, f"{self.base_url}{path}", timeout=self.timeout)
        except httpx.HTTPError as error:
            raise ExternalServiceError("booking-service no está disponible") from error

    @staticmethod
    def _raise_for_error(response: httpx.Response) -> None:
        if response.is_error:
            raise ExternalServiceError(
                f"booking-service respondió {response.status_code}: {response.text}"
            )
