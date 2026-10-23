# Contratos entre servicios

Cada servicio expone OpenAPI en `/docs`. Aquí solo están los contratos que **otros
servicios consumen**; cambiarlos exige avisar a los consumidores.

## REST (síncrono)

### user-service → `GET /users/{id}`

Consumido por: **booking-service** (¿existe el usuario?) y **notification-worker** (email).

```json
200 {
  "id": "uuid",
  "name": "Habith De León",
  "email": "habith@mail.com",
  "identification_type": "CC",
  "identification_number": "1043",
  "birthday_date": "1999-03-10",
  "created_at": "2026-10-23T13:00:00Z"
}
404 {"detail": "No existe el usuario ..."}
```

Campos que usan los consumidores: `id`, `name`, `email`.

### resources-service → `GET /resources/{id}`

Consumido por: **booking-service**.

```json
200 {
  "id": "uuid",
  "name": "Sala Caribe",
  "resource_type": "MEETING_ROOM",
  "capacity": 8,
  "price_per_hour": "50000.00",
  "is_active": true,
  "...": "..."
}
404 {"detail": "No existe el recurso ..."}
```

Campos que usan: `id`, `name`, `capacity`, `price_per_hour`, `is_active`.

### booking-service → `GET /bookings/{id}` y `POST /bookings/{id}/confirm`

Consumido por: **payment-service**.

```json
200 {
  "id": "uuid",
  "user_id": "uuid",
  "status": "PENDING | CONFIRMED | CANCELLED",
  "total_price": "100000.00",
  "...": "..."
}
POST /confirm → 200 (CONFIRMED) | 404 | 409 si no está PENDING
```

Campos que usan: `id`, `user_id`, `status`, `total_price`.

## Errores (todos los servicios)

| Código | Significado | Excepción base |
|---|---|---|
| 404 | No existe | `NotFoundError` |
| 409 | Choca con el estado actual (solapamiento, duplicado, transición) | `ConflictError` |
| 422 | Dato inválido / invariante violada | `DomainValidationError` |
| 503 | Un servicio del que dependo no responde | `ExternalServiceError` |

Formato: `{"detail": "mensaje"}`.

## Eventos (asíncrono · RabbitMQ)

- Exchange: `booking.events` (tipo `topic`, durable)
- Productor: **booking-service**
- Routing key = nombre del evento
- Entrega **al menos una vez**: los consumidores deben ser idempotentes por `event_id`

### Sobre común

```json
{
  "event": "booking.confirmed",
  "event_id": "uuid",
  "occurred_at": "2026-10-23 13:34:34.932538+00:00",
  "data": { }
}
```

### `booking.confirmed`

Cuándo: una reserva pasa a `CONFIRMED` (pago aprobado).

```json
"data": {
  "booking_id": "uuid",
  "user_id": "uuid",
  "resource_id": "uuid",
  "start_at": "2026-11-03 14:00:00-05:00",
  "end_at": "2026-11-03 16:00:00-05:00",
  "total_price": "100000.00"
}
```

### `booking.cancelled`

Cuándo: una reserva pasa a `CANCELLED` (libera el horario).

```json
"data": {
  "booking_id": "uuid",
  "user_id": "uuid",
  "resource_id": "uuid",
  "start_at": "...",
  "end_at": "..."
}
```

| Consumidor | Cola | Eventos |
|---|---|---|
| notification-service | `notification-service.booking-events` | `booking.confirmed`, `booking.cancelled` |
