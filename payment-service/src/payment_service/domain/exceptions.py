class DomainError(Exception):
    """Base de todos los errores de negocio de este servicio."""


class DomainValidationError(DomainError):
    """Se violó una invariante de una entidad o un dato de entrada es inválido."""


class NotFoundError(DomainError):
    """El recurso solicitado no existe."""


class ConflictError(DomainError):
    """La operación choca con el estado actual (duplicado, transición inválida...)."""


class InvalidPaymentError(DomainValidationError):
    pass


class PaymentNotFoundError(NotFoundError):
    def __init__(self, payment_id):
        super().__init__(f"No existe el pago {payment_id}")


class InvalidPaymentTransitionError(ConflictError):
    pass


class PaymentAlreadyApprovedError(ConflictError):
    def __init__(self, booking_id):
        super().__init__(f"La reserva {booking_id} ya tiene un pago aprobado")


class BookingNotFoundError(NotFoundError):
    def __init__(self, booking_id):
        super().__init__(f"No existe la reserva {booking_id}")


class BookingNotPayableError(ConflictError):
    def __init__(self, booking_id, status):
        super().__init__(f"La reserva {booking_id} no se puede pagar (estado: {status})")
