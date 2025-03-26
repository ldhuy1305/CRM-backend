from __future__ import absolute_import, unicode_literals

import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
from celery import Celery

app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

print("Registered tasks:", app.tasks)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def add(x, y):
    return x + y


@app.task
def send_notification_for_task(actor_id, recipient_id):
    from django_notification.models import Notification
    from django_notification.models.helper.enums.status_choices import NotificationStatus
    from authentication.models import User
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    # Create the notification
    actor = User.objects.get(id=actor_id)
    recipients = User.objects.get(id=recipient_id)
    notification = Notification.objects.create_notification(
        verb="Logged in to Admin panel",
        actor=actor,
        recipients=[recipients],
        description="",
        status=NotificationStatus.INFO,
        public=True,
        link="",
        is_sent=True,
    )

    # Send WebSocket message to the recipient's group
    channel_layer = get_channel_layer()
    for recipient in recipients:
        async_to_sync(channel_layer.group_send)(
            f'user_{recipient.id}',
            {
                'type': 'send_notification',
                'notification': {
                    'id': notification.id,
                    'verb': notification.verb,
                    'status': notification.status,
                    'description': notification.description,
                    'link': notification.link,
                }
            }
        )


@app.task
def shared_task():
    print("Task is running!")
    return "Done"


@app.task
def send_notification_task(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message
        }
    )
