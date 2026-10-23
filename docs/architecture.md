# Arquitectura

## 1. Arquitectura del sistema (microservicios)

```mermaid
flowchart LR
    client([Cliente / Swagger])

    subgraph sync [Comunicación síncrona · REST]
        users[user-service<br/>:8001]
        resources[resources-service<br/>:8002]
        bookings[booking-service<br/>:8003]
        payments[payment-service<br/>:8004]
        notifications[notification-service<br/>:8005]
    end

    mq[(RabbitMQ<br/>exchange booking.events)]
    worker[notification-worker]

    subgraph pg [PostgreSQL · un esquema por servicio]
        s1[(users)]
        s2[(resources)]
        s3[(bookings)]
        s4[(payments)]
        s5[(notifications)]
    end

    client --> users & resources & bookings & payments & notifications

    bookings -- GET /users/id --> users
    bookings -- GET /resources/id --> resources
    payments -- GET /bookings/id<br/>POST /bookings/id/confirm --> bookings

    bookings -- booking.confirmed<br/>booking.cancelled --> mq
    mq --> worker
    worker -- GET /users/id --> users

    users --- s1
    resources --- s2
    bookings --- s3
    payments --- s4
    notifications --- s5
    worker --- s5
```

### Por qué microservicios aquí

| Servicio | Responsabilidad única | Por qué está separado |
|---|---|---|
| user-service | Identidad y perfiles | Lo consultan todos; cambia poco |
| resources-service | Catálogo de recursos, precio, disponibilidad (activo/inactivo) | Lo administra otro actor (operaciones) |
| booking-service | Reglas de reserva, conflictos, estados | **Núcleo del dominio**; es el que más evoluciona |
| payment-service | Pagos simulados e integridad | Requisitos de seguridad y auditoría distintos |
| notification-service | Entrega de mensajes | Debe poder fallar sin tumbar las reservas (asíncrono) |

No se creó un servicio por tabla: `TimeSlot` y los estados viven dentro de booking.

### Propiedad de datos

- Cada servicio **solo lee y escribe su esquema**. Nadie consulta la base de otro.
- Las referencias entre servicios son **ids sin foreign key** (`user_id`, `resource_id`, `booking_id`).
- **No se comparten modelos ORM**: cada servicio tiene sus propios `models/` y `entities/`.
- Lo que un servicio necesita de otro lo obtiene por **contrato** (ver `contracts.md`) y lo
  representa con su propio DTO (`ResourceSnapshot`, `BookingSnapshot`, `UserContact`).

## 2. Flujo principal

```mermaid
sequenceDiagram
    actor C as Cliente
    participant B as booking
    participant U as user
    participant R as resources
    participant P as payment
    participant Q as RabbitMQ
    participant N as notification-worker

    C->>B: POST /bookings
    B->>U: GET /users/{id}
    B->>R: GET /resources/{id} (precio, capacidad, activo)
    B->>B: TimeSlot + Booking.schedule() + chequeo de solapamiento
    B-->>C: 201 PENDING (total calculado)

    C->>P: POST /payments {booking_id, token}
    P->>B: GET /bookings/{id} (monto y estado)
    P->>P: Pasarela simulada → APPROVED
    P->>B: POST /bookings/{id}/confirm
    B->>Q: booking.confirmed
    P-->>C: 201 APPROVED

    Q->>N: booking.confirmed
    N->>U: GET /users/{id} (email)
    N->>N: guarda notificación (idempotente por event_id) y envía email
```

## 3. Arquitectura interna (Clean Architecture, igual en los 5 servicios)

```mermaid
flowchart TB
    P[presentation<br/>routers · schemas · consumers · dependencies]
    A[application<br/>use_cases · dtos · ports]
    D[domain<br/>entities · value_objects · events · exceptions · repositories]
    I[infrastructure<br/>persistence · clients · messaging · database]

    P --> A --> D
    I -. implementa puertos .-> A
    I -. implementa puertos .-> D
    P -. composition root elige adaptadores .-> I
```

**Regla de dependencias**: las flechas apuntan al dominio. `domain/` no importa
FastAPI, SQLModel, httpx ni pika (se puede verificar con `grep`).

| Capa | Contiene | Ejemplo en booking-service |
|---|---|---|
| domain | Entidades con invariantes, value objects, eventos, excepciones, puertos de repositorio | `Booking.confirm()`, `TimeSlot.overlaps()`, `BookingConfirmed` |
| application | Casos de uso que orquestan, DTOs de entrada, puertos hacia el exterior | `CreateBooking`, `CreateBookingCommand`, `ResourceGateway` |
| infrastructure | Implementaciones concretas | `SQLModelBookingRepository`, `HttpResourceGateway`, `RabbitMQEventPublisher` |
| presentation | Adaptadores de entrada | `booking_router.py`, `booking_schemas.py`, `dependencies.py` |

## 4. La regla clave: evitar conflictos de disponibilidad

Defensa en dos niveles en booking-service:

1. **Dominio / aplicación**: `CreateBooking` busca reservas activas que se solapen y
   lanza `BookingConflictError` (409) con un mensaje claro.
2. **Base de datos**: restricción de exclusión, la única garantía real ante peticiones concurrentes:

```sql
EXCLUDE USING gist (
    resource_id WITH =,
    tstzrange(start_at, end_at, '[)') WITH &&
) WHERE (status <> 'CANCELLED')
```

El repositorio traduce el error `23P01` de Postgres al mismo `BookingConflictError`,
así la capa de presentación no se entera de qué nivel lo detectó.

Mismo patrón en payment-service para "un solo pago aprobado por reserva"
(índice único parcial) y en notification-service para "un evento, una notificación"
(`event_id` único).

## 5. Capacidad de evolución

| Cambio futuro | Qué se toca | Qué NO se toca |
|---|---|---|
| Pasarela real (Wompi/Stripe) | Nuevo adaptador `PaymentProcessor` | Dominio y casos de uso de pagos |
| Emails reales (SMTP/SES) | Nuevo `NotificationSender` | Worker, plantillas y casos de uso |
| Payment confirma por evento en vez de REST | Nuevo adaptador en booking/payment | Entidad `Booking` |
| Outbox para publicar eventos de forma confiable | Infraestructura de booking | Casos de uso (siguen usando `EventPublisher`) |
| Base separada por servicio | `DATABASE_URL` de cada servicio | Código |
