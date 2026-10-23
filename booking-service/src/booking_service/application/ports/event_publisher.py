from abc import ABC, abstractmethod

from booking_service.domain.events import DomainEvent


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None: ...
