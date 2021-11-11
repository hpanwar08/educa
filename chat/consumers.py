import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from chat.models import Message


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
        event_type = text_data_json['type']
        message = text_data_json['message']

        now = timezone.now()

        if event_type == 'fetch_messages':
            # fetch old messages
            self.fetch_messages(text_data_json)
        else:
            Message.objects.create(
                creator=self.user,
                content=message,
                group_name=self.room_group_name,
            )
            # send message to group
            async_to_sync(self.channel_layer.group_send)(self.room_group_name,
                                                         {'type': 'chat_message',
                                                          'content': message,
                                                          'creator': self.user.email,
                                                          'created_at': now.isoformat()})

    def chat_message(self, event):
        self.send(text_data=json.dumps({'type': 'chat_message', 'message': [event]}))

    def fetch_messages(self, data):
        messages = reversed(Message.objects.filter(group_name=self.room_group_name)[:10])
        result = []
        for message in messages:
            msg = message.to_json()
            msg['type'] = 'all_message'
            result.append(msg)
            
        self.send(json.dumps({'type': 'all_message', 'message': result}))
