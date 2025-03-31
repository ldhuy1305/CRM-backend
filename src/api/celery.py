from __future__ import absolute_import, unicode_literals

import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
from celery import Celery

app = Celery('api')
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    broker_url=os.getenv("CELERY_BROKER_URL", 'redis://redis:6379/0'),
    result_backend=os.getenv("CELERY_RESULT_BACKEND", 'redis://redis:6379/0'),
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='Asia/Ho_Chi_Minh',
    broker_connection_retry_on_startup=True,
)

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

app.autodiscover_tasks()

@app.task
def send_notification_for_task(actor_id : int , recipient_ids: str):
    from django_notification.models import Notification
    from django_notification.models.helper.enums.status_choices import NotificationStatus
    from authentication.models import User
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    # Create the notification

    # Get list id of recipients
    recipient_ids = list(map(int,recipient_ids.split(',')))

    # Actor and recipents
    actor = User.objects.get(id=actor_id)
    recipients = User.objects.filter(id__in=recipient_ids)

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
        channel_layer = get_channel_layer()
        user_id = actor_id
        group_name = f"user_{user_id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "notification": "notification",
            }
        )


@app.task
def shared_task():
    print("This is a periodic task running every minute!")
