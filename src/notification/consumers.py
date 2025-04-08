import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        notification = event['notification']

        template = Template('<div class="notification"><p>{{notification}}</p></div>')
        context = Context({"notification": notification})
        rendered_notification = template.render(context)

        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "notification": rendered_notification
                }
            )
        )
