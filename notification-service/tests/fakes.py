from notification_service.application.exceptions import DeliveryError
from notification_service.application.ports.notification_sender import NotificationSender
from notification_service.application.ports.user_directory import UserContact, UserDirectory
from notification_service.domain.repositories.notification_repository import (
    NotificationRepository,
)


class InMemoryNotificationRepository(NotificationRepository):
    def __init__(self):
        self.items = {}

    def add(self, notification):
        self.items[notification.id] = notification
        return notification

    def get_by_id(self, notification_id):
        return self.items.get(notification_id)

    def get_by_event_id(self, event_id):
        return next((n for n in self.items.values() if n.event_id == event_id), None)

    def list(self, user_id=None, reference_id=None):
        return [
            n
            for n in self.items.values()
            if user_id in (None, n.user_id) and reference_id in (None, n.reference_id)
        ]


class SpySender(NotificationSender):
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    def send(self, notification):
        if self.fail:
            raise DeliveryError("SMTP caído")
        self.sent.append(notification)


class FakeUserDirectory(UserDirectory):
    def __init__(self, contacts):
        self.contacts = contacts

    def get_contact(self, user_id):
        return self.contacts.get(user_id)


def contact():
    return UserContact(name="Ana", email="ana@mail.com")
