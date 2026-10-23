from booking_service.domain.entities.booking import Booking, BookingStatus
from booking_service.domain.value_objects.time_slot import TimeSlot
from booking_service.infrastructure.persistence.models.booking_model import BookingModel


def to_domain(model: BookingModel) -> Booking:
    return Booking(
        id=model.id,
        user_id=model.user_id,
        resource_id=model.resource_id,
        slot=TimeSlot(model.start_at, model.end_at),
        attendees=model.attendees,
        total_price=model.total_price,
        status=BookingStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def apply_to_model(booking: Booking, model: BookingModel) -> BookingModel:
    model.user_id = booking.user_id
    model.resource_id = booking.resource_id
    model.start_at = booking.slot.start_at
    model.end_at = booking.slot.end_at
    model.attendees = booking.attendees
    model.total_price = booking.total_price
    model.status = booking.status.value
    model.created_at = booking.created_at
    model.updated_at = booking.updated_at
    return model
