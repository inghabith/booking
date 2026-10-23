from booking_service.application.ports.event_publisher import EventPublisher
from booking_service.application.ports.resource_gateway import ResourceGateway
from booking_service.application.ports.user_gateway import UserGateway
from booking_service.domain.entities.booking import BookingStatus
from booking_service.domain.repositories.booking_repository import BookingRepository


class InMemoryBookingRepository(BookingRepository):
    def __init__(self):
        self.bookings = {}

    def add(self, booking):
        self.bookings[booking.id] = booking
        return booking

    def update(self, booking):
        self.bookings[booking.id] = booking
        return booking

    def get_by_id(self, booking_id):
        return self.bookings.get(booking_id)

    def find_active_overlapping(self, resource_id, slot):
        return [
            b
            for b in self.bookings.values()
            if b.resource_id == resource_id
            and b.status != BookingStatus.CANCELLED
            and b.slot.overlaps(slot)
        ]

    def list(self, user_id=None, resource_id=None, status=None):
        result = list(self.bookings.values())
        if user_id:
            result = [b for b in result if b.user_id == user_id]
        if resource_id:
            result = [b for b in result if b.resource_id == resource_id]
        if status:
            result = [b for b in result if b.status == status]
        return result


class FakeResourceGateway(ResourceGateway):
    def __init__(self, *resources):
        self.resources = {r.id: r for r in resources}

    def get(self, resource_id):
        return self.resources.get(resource_id)


class FakeUserGateway(UserGateway):
    def __init__(self, *user_ids):
        self.user_ids = set(user_ids)

    def exists(self, user_id):
        return user_id in self.user_ids


class SpyEventPublisher(EventPublisher):
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)
