from collections.abc import Callable
from datetime import datetime

from booking_service.application.dtos import CreateBookingCommand
from booking_service.application.ports.resource_gateway import ResourceGateway
from booking_service.application.ports.user_gateway import UserGateway
from booking_service.domain.entities.booking import Booking
from booking_service.domain.exceptions import (
    BookingConflictError,
    ResourceNotFoundError,
    ResourceUnavailableError,
    UserNotFoundError,
)
from booking_service.domain.repositories.booking_repository import BookingRepository
from booking_service.domain.value_objects.time_slot import TimeSlot
from booking_service.shared.time import utc_now


class CreateBooking:
    def __init__(
        self,
        booking_repository: BookingRepository,
        resource_gateway: ResourceGateway,
        user_gateway: UserGateway,
        clock: Callable[[], datetime] = utc_now,
    ):
        self.booking_repository = booking_repository
        self.resource_gateway = resource_gateway
        self.user_gateway = user_gateway
        self.clock = clock

    def execute(self, command: CreateBookingCommand) -> Booking:
        slot = TimeSlot(command.start_at, command.end_at)

        # 1. Datos de otros servicios, vía sus contratos (nunca su base de datos).
        if not self.user_gateway.exists(command.user_id):
            raise UserNotFoundError(command.user_id)

        resource = self.resource_gateway.get(command.resource_id)
        if resource is None:
            raise ResourceNotFoundError(command.resource_id)
        if not resource.is_active:
            raise ResourceUnavailableError(command.resource_id)

        # 2. Reglas de la reserva (precio, futuro, capacidad) en la entidad.
        booking = Booking.schedule(
            user_id=command.user_id,
            resource_id=command.resource_id,
            slot=slot,
            price_per_hour=resource.price_per_hour,
            resource_capacity=resource.capacity,
            attendees=command.attendees,
            now=self.clock(),
        )

        # 3. Regla clave: sin solapamientos. Esta consulta da un error claro en el
        #    caso normal; la exclusion constraint de Postgres cubre las carreras
        #    (dos peticiones simultáneas) y el repositorio la traduce al mismo error.
        overlapping = self.booking_repository.find_active_overlapping(resource.id, slot)
        if any(booking.conflicts_with(other) for other in overlapping):
            raise BookingConflictError(resource.id)

        return self.booking_repository.add(booking)
