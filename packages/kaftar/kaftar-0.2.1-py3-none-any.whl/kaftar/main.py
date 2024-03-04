from uuid import UUID

from celery import Celery

from .schemas import FirebaseNotification


class Notification:
    def __init__(self, service_name: str, broker_url) -> None:
        self.app = Celery(service_name, broker=broker_url)
        self.service_name = service_name

    def send_notification(
            self,
            body: dict,
            recipients: list[dict],
            send_datetime: int,
            group_uuid: UUID = None
    ) -> None:
        if group_uuid:
            group_uuid = str(group_uuid)
        if type(send_datetime) is not int:
            raise ValueError("send_datetime must be int")
        if "subject" not in body or "content" not in body:
            raise ValueError("subject or content missing")

        self.app.send_task('notification.notification.send_notification',
                           (body,
                            recipients,
                            self.service_name,
                            send_datetime,
                            group_uuid),
                           queue='notification')

    def send_firebase_notification(
            self,
            notification_data: FirebaseNotification,
            recipients: list[UUID]
    ):
        self.app.send_task('notification.notification.send_firebase_notification',
                           (notification_data,
                            recipients,),
                           queue='notification')

    def delete_notification(
            self,
            message_uuid: UUID
    ) -> None:
        self.app.send_task('notification.notification.delete_notification',
                           (message_uuid,),
                           queue='notification')

    def delete_group_notification(
            self,
            group_uuid: UUID
    ) -> None:
        self.app.send_task('notification.notification.delete_group_notification',
                           (group_uuid,),
                           queue='notification')
