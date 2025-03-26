from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_notification.models.notification import Notification


def create_notification(verb, actor, recipient, description, status, public, link, is_sent):
    # create notification
    notification = Notification.objects.create_notification(
        verb=verb,
        actor=actor,
        recipients=[recipient],
        description=description,
        status=status,
        public=public,
        link=link,
        is_sent=is_sent,
    )

    # Send to recipient
    channel_layer = get_channel_layer()
    for user in [recipient]:
        async_to_sync(channel_layer.group_send)(
            f'user_{user.id}',
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
    return notification
