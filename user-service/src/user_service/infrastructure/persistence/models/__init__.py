"""Modelos de tabla (SQLModel). Importarlos aquí los registra para Alembic."""
from user_service.infrastructure.persistence.models.user_model import UserModel

__all__ = ["UserModel"]
