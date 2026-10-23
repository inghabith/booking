"""Engine y unidad de trabajo. Aquí, y solo aquí, se hace commit o rollback."""
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from user_service.shared.config import DATABASE_URL


@lru_cache
def get_engine() -> Engine:
    # Se crea al primer uso: los tests unitarios no necesitan base de datos.
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL no está configurada en el archivo .env")
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session():
    """Dependencia de FastAPI: una sesión por petición."""
    session = Session(get_engine())
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def session_scope():
    """Lo mismo que get_session, para usar fuera de FastAPI (workers, scripts)."""
    yield from get_session()
