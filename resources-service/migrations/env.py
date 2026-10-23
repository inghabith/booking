"""Alembic de resources-service.

Propiedad de datos: este servicio solo es dueño del esquema "resources".
Aunque todos los servicios usen la misma base (p. ej. Supabase), cada uno:
  - crea y migra únicamente su esquema,
  - guarda su versión de Alembic dentro de su esquema,
  - ignora las tablas de los demás (el autogenerate nunca propone borrarlas).
"""
from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

from resources_service.infrastructure.database.session import get_engine
from resources_service.infrastructure.persistence import models  # noqa: F401  (registra las tablas)
from resources_service.shared.config import DB_SCHEMA

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == DB_SCHEMA
    return True


def run_migrations_online() -> None:
    engine = get_engine()

    with engine.connect() as connection:
        # La tabla de versiones vive en el esquema: debe existir antes de migrar.
        connection.exec_driver_sql(f'CREATE SCHEMA IF NOT EXISTS "{DB_SCHEMA}"')
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            version_table_schema=DB_SCHEMA,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise SystemExit("Este proyecto solo usa migraciones online: alembic upgrade head")

run_migrations_online()
