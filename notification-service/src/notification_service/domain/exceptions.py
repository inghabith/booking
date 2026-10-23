class DomainError(Exception):
    """Base de todos los errores de negocio de este servicio."""


class DomainValidationError(DomainError):
    """Se violó una invariante de una entidad o un dato de entrada es inválido."""


class NotFoundError(DomainError):
    """El recurso solicitado no existe."""


class ConflictError(DomainError):
    """La operación choca con el estado actual (duplicado, transición inválida...)."""


class InvalidNotificationError(DomainValidationError):
    pass


class NotificationNotFoundError(NotFoundError):
    def __init__(self, notification_id):
        super().__init__(f"No existe la notificación {notification_id}")


class InvalidNotificationTransitionError(ConflictError):
    pass


class UnsupportedEventError(DomainValidationError):
    pass
