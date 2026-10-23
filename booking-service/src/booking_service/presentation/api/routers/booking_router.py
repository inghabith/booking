from uuid import UUID

from fastapi import APIRouter, Depends

from booking_service.application.dtos import BookingFilters, CreateBookingCommand
from booking_service.application.use_cases.cancel_booking import CancelBooking
from booking_service.application.use_cases.confirm_booking import ConfirmBooking
from booking_service.application.use_cases.create_booking import CreateBooking
from booking_service.application.use_cases.get_booking import GetBooking
from booking_service.application.use_cases.list_bookings import ListBookings
from booking_service.domain.entities.booking import Booking, BookingStatus
from booking_service.presentation.api.dependencies import (
    get_cancel_booking,
    get_confirm_booking,
    get_create_booking,
    get_get_booking,
    get_list_bookings,
)
from booking_service.presentation.api.schemas.booking_schemas import (
    BookingCreateRequest,
    BookingResponse,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", status_code=201)
def create_booking(
    payload: BookingCreateRequest, use_case: CreateBooking = Depends(get_create_booking)
) -> BookingResponse:
    command = CreateBookingCommand(**payload.model_dump())
    return to_response(use_case.execute(command))


@router.get("")
def list_bookings(
    user_id: UUID | None = None,
    resource_id: UUID | None = None,
    status: BookingStatus | None = None,
    use_case: ListBookings = Depends(get_list_bookings),
) -> list[BookingResponse]:
    filters = BookingFilters(user_id=user_id, resource_id=resource_id, status=status)
    return [to_response(booking) for booking in use_case.execute(filters)]


@router.get("/{booking_id}")
def get_booking(
    booking_id: UUID, use_case: GetBooking = Depends(get_get_booking)
) -> BookingResponse:
    return to_response(use_case.execute(booking_id))


@router.post("/{booking_id}/confirm")
def confirm_booking(
    booking_id: UUID, use_case: ConfirmBooking = Depends(get_confirm_booking)
) -> BookingResponse:
    return to_response(use_case.execute(booking_id))


@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: UUID, use_case: CancelBooking = Depends(get_cancel_booking)
) -> BookingResponse:
    return to_response(use_case.execute(booking_id))


def to_response(booking: Booking) -> BookingResponse:
    return BookingResponse(
        id=booking.id,
        user_id=booking.user_id,
        resource_id=booking.resource_id,
        start_at=booking.slot.start_at,
        end_at=booking.slot.end_at,
        attendees=booking.attendees,
        total_price=booking.total_price,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )
