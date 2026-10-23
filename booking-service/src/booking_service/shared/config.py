"""Configuración del servicio leída del entorno (.env)."""
import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str) -> str:
    # SQLAlchemy necesita saber que el driver es psycopg 3.
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


SERVICE_NAME = "booking-service"
DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", "").strip())

# Esquema de Postgres del que este servicio es dueño exclusivo.
DB_SCHEMA = "bookings"

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8001").rstrip("/")
RESOURCES_SERVICE_URL = os.getenv("RESOURCES_SERVICE_URL", "http://localhost:8002").rstrip("/")
HTTP_TIMEOUT_SECONDS = float(os.getenv("HTTP_TIMEOUT_SECONDS", "3"))

EVENT_PUBLISHER = os.getenv("EVENT_PUBLISHER", "logging")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
EVENTS_EXCHANGE = "booking.events"
