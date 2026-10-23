class DomainError(Exception):
    """Base de todos los errores de negocio de este servicio."""


class DomainValidationError(DomainError):
    """Se violó una invariante de una entidad o un dato de entrada es inválido."""


class NotFoundError(DomainError):
    """El recurso solicitado no existe."""


class ConflictError(DomainError):
    """La operación choca con el estado actual (duplicado, transición inválida...)."""


class InvalidTimeSlotError(DomainValidationError):
    pass


class InvalidBookingError(DomainValidationError):
    pass


class BookingNotFoundError(NotFoundError):
    def __init__(self, booking_id):
        super().__init__(f"No existe la reserva {booking_id}")


class BookingConflictError(ConflictError):
    """La regla clave del dominio: dos reservas activas no se solapan en un recurso."""

    def __init__(self, resource_id=None):
        message = "El recurso ya está reservado en ese horario"
        if resource_id is not None:
            message = f"El recurso {resource_id} ya está reservado en ese horario"
        super().__init__(message)


class InvalidBookingTransitionError(ConflictError):
    pass


# Referencias a datos de OTROS servicios (los validamos vía sus contratos).
class UserNotFoundError(NotFoundError):
    def __init__(self, user_id):
        super().__init__(f"No existe el usuario {user_id}")


class ResourceNotFoundError(NotFoundError):
    def __init__(self, resource_id):
        super().__init__(f"No existe el recurso {resource_id}")


class ResourceUnavailableError(ConflictError):
    def __init__(self, resource_id):
        super().__init__(f"El recurso {resource_id} no está disponible para reservas")
