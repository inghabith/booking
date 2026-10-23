"""Configuración del servicio leída del entorno (.env)."""
import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str) -> str:
    # SQLAlchemy necesita saber que el driver es psycopg 3.
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


SERVICE_NAME = "resources-service"
DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", "").strip())

# Esquema de Postgres del que este servicio es dueño exclusivo.
DB_SCHEMA = "resources"
