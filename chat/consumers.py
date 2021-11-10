import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        # get course id
        self.id = self.scope['url_route']['kwargs']['course_id']
        # make group name
        self.room_group_name = f"chat_{self.id}"
        # add channel to group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, code):
        # remove channel from group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        now = timezone.now()

        # send message to group
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'chat_message', 'message': message,
                                                                            'user': self.user.email,
                                                                            'datetime': now.isoformat()})
        # self.send(text_data=json.dumps({'message': message}))

    def chat_message(self, event):
        # message = event['message']
        self.send(text_data=json.dumps(event))
