import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AlarmConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            return

        self.group_name = "alarm_" + str(self.user.id)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def notify_alarm(self, event):
        self.send(text_data=json.dumps({
            "id": event["id"],
            "message": event["message"],
        }))
