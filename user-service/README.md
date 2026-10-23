# user-service

Dueño de la **identidad y perfiles** de usuario. Esquema de base de datos: `users`.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/users` | Crea un usuario (email e identificación únicos) |
| GET | `/users` | Lista usuarios (`limit`, `offset`) |
| GET | `/users/{id}` | Consulta un usuario (lo usan booking y notification) |

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn user_service.main:app --reload --port 8001
uv run pytest
```
