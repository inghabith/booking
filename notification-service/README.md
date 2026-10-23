# notification-service

Dueño de las **notificaciones**. Esquema: `notifications`.

Tiene **dos adaptadores de entrada** que llegan a los mismos casos de uso:

1. **API REST**: `POST /notifications`, `GET /notifications`, `GET /notifications/{id}`.
2. **Worker RabbitMQ**: consume `booking.confirmed` y `booking.cancelled` del exchange
   `booking.events` (cola `notification-service.booking-events`).

Los eventos traen `user_id`, no el email: el email se consulta a user-service
(`GET /users/{id}`).

**Idempotencia**: RabbitMQ entrega *al menos una vez*. Cada notificación guarda el
`event_id` (único en la base), así un mensaje repetido no genera un segundo email.

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn notification_service.main:app --reload --port 8005
uv run python -m notification_service.presentation.consumers.booking_events_consumer
uv run pytest
```
