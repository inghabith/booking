"""Traduce errores de dominio/aplicación a respuestas HTTP.

Así los routers no se llenan de try/except y el dominio no conoce HTTP.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from resources_service.application.exceptions import ExternalServiceError
from resources_service.domain.exceptions import (
    ConflictError,
    DomainValidationError,
    NotFoundError,
)

_STATUS_BY_ERROR = {
    DomainValidationError: 422,
    NotFoundError: 404,
    ConflictError: 409,
    ExternalServiceError: 503,
}


def register_error_handlers(app: FastAPI) -> None:
    for error_class, status_code in _STATUS_BY_ERROR.items():
        app.add_exception_handler(error_class, _handler(status_code))


def _handler(status_code: int):
    async def handle(request: Request, error: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(error)})

    return handle
