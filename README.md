# Booking Platform · Plataforma de reservas en microservicios

Sistema de reservas de salas y recursos con **5 microservicios en FastAPI**, cada uno con
**Clean Architecture**, su propio esquema de PostgreSQL, migraciones con Alembic,
comunicación REST y eventos por RabbitMQ.

> Basado en los principios de `ecommerce_microservices` (instructor), aplicados al dominio
> de reservas y corrigiendo: SQLModel fuera del dominio, reglas de negocio en las entidades,
> DTOs entre router y caso de uso, un esquema por servicio y precios/montos que nunca vienen del cliente.

| Servicio | Puerto | Esquema | Responsabilidad |
|---|---|---|---|
| [user-service](user-service/) | 8001 | `users` | Identidad y perfiles |
| [resources-service](resources-service/) | 8002 | `resources` | Recursos, características, precio y disponibilidad |
| [booking-service](booking-service/) | 8003 | `bookings` | Reglas de reserva, **conflictos** y estados |
| [payment-service](payment-service/) | 8004 | `payments` | Pagos simulados e integridad de transacciones |
| [notification-service](notification-service/) | 8005 | `notifications` | Notificaciones tras confirmaciones y cambios |

📐 Arquitectura y diagramas: [`docs/architecture.md`](docs/architecture.md) ·
📜 Contratos entre servicios: [`docs/contracts.md`](docs/contracts.md)

## Regla clave del dominio

**Dos reservas activas del mismo recurso no pueden solaparse.** Se valida en el dominio
(`TimeSlot.overlaps`) y se **garantiza en Postgres** con una restricción `EXCLUDE USING gist`,
que cubre las peticiones concurrentes. Los intervalos son `[inicio, fin)`, así que reservas
contiguas (10–11 y 11–12) son válidas.

## Estructura de cada servicio

```
<servicio>/
├── src/<paquete>/
│   ├── domain/            # Python puro: entidades, value objects, eventos, excepciones,
│   │                      #   puertos de repositorio. NO importa frameworks.
│   ├── application/       # Casos de uso, DTOs y puertos hacia otros servicios.
│   ├── infrastructure/    # SQLModel, mappers, clientes HTTP, RabbitMQ, sesión de BD.
│   ├── presentation/      # Routers, schemas Pydantic, error handlers, consumers,
│   │                      #   dependencies.py (composition root).
│   ├── shared/            # config (.env) y utilidades sin lógica de negocio.
│   └── main.py
├── migrations/            # Alembic, limitado al esquema del servicio
├── tests/                 # Unitarios con fakes en memoria (no necesitan BD)
├── Dockerfile
├── pyproject.toml / uv.lock
└── .env.example
```

Dependencias: `presentation → application → domain`; `infrastructure` implementa los
puertos. Verificable con:

```bash
grep -rnE "^(from|import) (fastapi|sqlmodel|sqlalchemy|httpx|pika|pydantic)" */src/*/domain/
# (sin resultados)
```

## Cómo ejecutarlo

### Opción A · Docker (todo junto)

```bash
docker compose up --build
```

Levanta Postgres, RabbitMQ (consola en http://localhost:15672, guest/guest), los 5 servicios
y el worker de notificaciones. Cada contenedor corre `alembic upgrade head` al iniciar.

### Opción B · Local con uv (p. ej. contra Supabase)

En cada servicio:

```bash
cd user-service
cp .env.example .env          # pon tu DATABASE_URL
uv sync
uv run alembic upgrade head
uv run uvicorn user_service.main:app --reload --port 8001
```

Todos pueden usar **la misma** `DATABASE_URL`: cada uno crea y migra solo su esquema.
Sin RabbitMQ, deja `EVENT_PUBLISHER=logging` en booking-service (los eventos se imprimen).

### Tests

```bash
cd booking-service && uv run pytest
# Integración contra Postgres real (restricción anti-solapamiento):
TEST_DATABASE_URL=postgresql://... uv run pytest tests/integration
```

## Prueba rápida del flujo completo

```bash
J='content-type: application/json'

# 1. Usuario y recurso
curl -XPOST localhost:8001/users -H "$J" -d '{"name":"Habith","email":"habith@mail.com","identification_type":"CC","identification_number":"1043","birthday_date":"1999-03-10"}'
curl -XPOST localhost:8002/resources -H "$J" -d '{"name":"Sala Caribe","resource_type":"MEETING_ROOM","capacity":8,"price_per_hour":"50000"}'

# 2. Reserva (el total lo calcula el sistema: 2 h × 50.000 = 100.000)
curl -XPOST localhost:8003/bookings -H "$J" -d '{"user_id":"<USER>","resource_id":"<RES>","start_at":"2026-11-03T14:00:00-05:00","end_at":"2026-11-03T16:00:00-05:00","attendees":4}'

# 3. Otra que se cruza → 409
curl -XPOST localhost:8003/bookings -H "$J" -d '{"user_id":"<USER>","resource_id":"<RES>","start_at":"2026-11-03T15:00:00-05:00","end_at":"2026-11-03T17:00:00-05:00"}'

# 4. Pago (tok_declined = rechazado) → aprobado confirma la reserva y publica booking.confirmed
curl -XPOST localhost:8004/payments -H "$J" -d '{"booking_id":"<BOOKING>","payment_token":"tok_visa"}'

# 5. Email "enviado" por el worker
curl "localhost:8005/notifications?reference_id=<BOOKING>"
```

## Entregables y criterios de aceptación

| Entregable / criterio | Dónde |
|---|---|
| Diagrama de arquitectura del sistema | `docs/architecture.md` |
| Responsabilidades y límites de servicios | tabla de arriba + `docs/architecture.md` §1 |
| Estructura inicial del repositorio y README | este archivo + README de cada servicio |
| users-service y bookings-service ejecutables | los 5 servicios son ejecutables y tienen tests |
| Contratos iniciales entre servicios | `docs/contracts.md` |
| Arquitectura justificada por el dominio | `docs/architecture.md` §1 |
| Propiedad de datos / no compartir ORM | un esquema por servicio, ids sin FK, modelos propios |
| Clean Architecture en cada servicio | misma estructura de capas en los 5 |
| Evolución sin cambiar la arquitectura | `docs/architecture.md` §5 |

## Pendiente para las siguientes sesiones

Patrones de diseño · Testing y SonarQube · Ciberseguridad (auth, contraseñas en
user-service) · Idempotencia en `POST /payments` · Rate limiting y resiliencia
(reintentos/circuit breaker en clientes HTTP) · Outbox y dead-letter queue · Observabilidad ·
CI/CD con GHCR · Despliegue en AWS ECS Fargate.

## Migración desde la versión anterior de user-service

La tabla antigua `public.usr_users` y `public.alembic_version` quedaron de la primera
migración. La nueva vive en `users.users`. Si no tienes datos que conservar:

```sql
DROP TABLE IF EXISTS public.usr_users;
DROP TABLE IF EXISTS public.alembic_version;
```
