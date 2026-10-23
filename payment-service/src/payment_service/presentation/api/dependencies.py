"""Composition root."""
from fastapi import Depends

from payment_service.application.ports.booking_gateway import BookingGateway
from payment_service.application.ports.payment_processor import PaymentProcessor
from payment_service.application.use_cases.create_payment import CreatePayment
from payment_service.application.use_cases.get_payment import GetPayment
from payment_service.application.use_cases.list_payments import ListPayments
from payment_service.domain.repositories.payment_repository import PaymentRepository
from payment_service.infrastructure.clients.http_booking_gateway import HttpBookingGateway
from payment_service.infrastructure.database.session import get_session
from payment_service.infrastructure.persistence.repositories.sqlmodel_payment_repository import (
    SQLModelPaymentRepository,
)
from payment_service.infrastructure.processors.simulated_payment_processor import (
    SimulatedPaymentProcessor,
)
from payment_service.shared import config


def get_payment_repository(
    session=Depends(get_session, scope="function"),
) -> PaymentRepository:
    return SQLModelPaymentRepository(session)


def get_booking_gateway() -> BookingGateway:
    return HttpBookingGateway(config.BOOKINGS_SERVICE_URL, config.HTTP_TIMEOUT_SECONDS)


def get_payment_processor() -> PaymentProcessor:
    return SimulatedPaymentProcessor()


def get_create_payment(
    repository=Depends(get_payment_repository),
    bookings=Depends(get_booking_gateway),
    processor=Depends(get_payment_processor),
) -> CreatePayment:
    return CreatePayment(repository, bookings, processor)


def get_get_payment(repository=Depends(get_payment_repository)) -> GetPayment:
    return GetPayment(repository)


def get_list_payments(repository=Depends(get_payment_repository)) -> ListPayments:
    return ListPayments(repository)
