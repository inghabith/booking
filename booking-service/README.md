# booking-service

Dueño de las **reservas**: reglas de reserva, detección de conflictos y estados.
Esquema: `bookings`.

## Regla clave: no solapamiento

Dos reservas activas (`PENDING` o `CONFIRMED`) de un mismo recurso no pueden cruzarse.
Se protege en dos niveles:

1. **Dominio**: `TimeSlot.overlaps()` + `Booking.conflicts_with()`, verificado en
   `CreateBooking` → error claro `409`.
2. **Base de datos**: `EXCLUDE USING gist (resource_id WITH =, tstzrange(start_at, end_at, '[)') WITH &&)`
   en la migración `0001`. Cubre las carreras (dos peticiones al mismo tiempo).
   El repositorio traduce el error `23P01` a `BookingConflictError`.

Intervalos semiabiertos `[inicio, fin)`: 10:00–11:00 y 11:00–12:00 **sí** se permiten.

## Estados

```
PENDING ──confirm()──▶ CONFIRMED
   │                       │
   └──────cancel()─────────┴──▶ CANCELLED   (libera el horario)
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/bookings` | Crea una reserva `PENDING` (el total lo calcula el sistema) |
| GET | `/bookings` | Lista (`user_id`, `resource_id`, `status`) |
| GET | `/bookings/{id}` | Consulta (lo usa payment-service) |
| POST | `/bookings/{id}/confirm` | Confirma (lo llama payment-service) → evento `booking.confirmed` |
| POST | `/bookings/{id}/cancel` | Cancela → evento `booking.cancelled` |

## Dependencias de otros servicios

| Servicio | Contrato | Para qué |
|---|---|---|
| user-service | `GET /users/{id}` | Validar que el usuario existe |
| resources-service | `GET /resources/{id}` | Precio, capacidad y si está activo |
| RabbitMQ | exchange `booking.events` (topic) | Publicar eventos |

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn booking_service.main:app --reload --port 8003
uv run pytest                                   # unitarios
TEST_DATABASE_URL=... uv run pytest tests/integration
```
