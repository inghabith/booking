"""Pasarela simulada, al estilo de los tokens de prueba de Stripe/Wompi.

    tok_declined -> rechazado (fondos insuficientes)
    tok_error    -> rechazado (error de la pasarela)
    cualquier otro token -> aprobado
"""
from decimal import Decimal

from payment_service.application.ports.payment_processor import ChargeResult, PaymentProcessor
from payment_service.domain.entities.payment import PaymentMethod

DECLINED_TOKENS = {
    "tok_declined": "Fondos insuficientes",
    "tok_error": "Error en la pasarela de pagos",
}


class SimulatedPaymentProcessor(PaymentProcessor):
    def charge(self, amount: Decimal, method: PaymentMethod, payment_token: str) -> ChargeResult:
        reason = DECLINED_TOKENS.get(payment_token)
        if reason:
            return ChargeResult(approved=False, reason=reason)
        return ChargeResult(approved=True)
