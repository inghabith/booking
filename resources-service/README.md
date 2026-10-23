# resources-service

Dueño de los **recursos reservables** (salas, escritorios, equipos): características,
precio por hora y si están disponibles (activos). Esquema: `resources`.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/resources` | Crea un recurso |
| GET | `/resources` | Lista (`resource_type`, `only_active`, `min_capacity`) |
| GET | `/resources/{id}` | Consulta un recurso (lo usa booking-service) |
| POST | `/resources/{id}/activate` | Lo habilita para reservas |
| POST | `/resources/{id}/deactivate` | Lo saca de servicio (mantenimiento) |

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn resources_service.main:app --reload --port 8002
uv run pytest
```
