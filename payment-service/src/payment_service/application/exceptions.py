"""Errores de la capa de aplicación (no son reglas de negocio)."""


class ExternalServiceError(Exception):
    """Un servicio del que dependemos no respondió o respondió con error."""
