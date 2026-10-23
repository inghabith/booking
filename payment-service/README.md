# payment-service

Dueño de los **pagos** (simulados) y de la integridad de las transacciones.
Esquema: `payments`.

- El monto **lo dicta booking-service** (`total_price`), nunca el cliente.
- Solo se pagan reservas `PENDING`.
- Máximo **un pago aprobado por reserva**: validado en `CreatePayment` y garantizado
  con un índice único parcial (`WHERE status = 'APPROVED'`).
- Un pago aprobado llama a `POST /bookings/{id}/confirm`.

Tokens de prueba: `tok_declined` (fondos insuficientes), `tok_error` (pasarela);
cualquier otro → aprobado.

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/payments` | Paga una reserva `{booking_id, method, payment_token}` |
| GET | `/payments` | Lista (`booking_id`) |
| GET | `/payments/{id}` | Consulta un pago |

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn payment_service.main:app --reload --port 8004
uv run pytest
```
