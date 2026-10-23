import uuid

from notification_service.application.dtos import SendNotificationCommand
from notification_service.application.use_cases.send_notification import SendNotification
from notification_service.domain.entities.notification import NotificationStatus
from tests.fakes import InMemoryNotificationRepository, SpySender


def cmd(event_id=None):
    return SendNotificationCommand(
        recipient="ana@mail.com", subject="Hola", body="Mensaje", event_id=event_id
    )


def test_envia_y_marca_enviada():
    repo, sender = InMemoryNotificationRepository(), SpySender()
    notification = SendNotification(repo, sender).execute(cmd())
    assert notification.status == NotificationStatus.SENT
    assert len(sender.sent) == 1


def test_fallo_de_entrega_queda_registrado():
    repo = InMemoryNotificationRepository()
    notification = SendNotification(repo, SpySender(fail=True)).execute(cmd())
    assert notification.status == NotificationStatus.FAILED
    assert repo.get_by_id(notification.id).error == "SMTP caído"


def test_mismo_evento_no_duplica():
    repo, sender = InMemoryNotificationRepository(), SpySender()
    event_id = uuid.uuid4()
    first = SendNotification(repo, sender).execute(cmd(event_id))
    second = SendNotification(repo, sender).execute(cmd(event_id))
    assert first.id == second.id
    assert len(sender.sent) == 1
