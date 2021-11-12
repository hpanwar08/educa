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
            msg_id = self.save_chat(message)
            # send message to group
            async_to_sync(self.channel_layer.group_send)(self.room_group_name,
                                                         {'type': 'chat_message',
                                                          'message_id': msg_id,
                                                          'content': message,
                                                          'creator': self.user.email,
                                                          'created_at': now.isoformat()})

    def chat_message(self, event):
        self.send(text_data=json.dumps({'type': 'chat_message', 'message': [event]}))

    def fetch_messages(self, data):
        messages = self.get_last_n_messages()
        result = []
        for message in messages:
            msg = self.message_to_json(message)
            msg['type'] = 'all_message'
            result.append(msg)

        self.send(json.dumps({'type': 'all_message', 'message': result}))

    def save_chat(self, message):
        msg = Message.objects.create(
            creator=self.user,
            content=message,
            group_name=self.room_group_name,
        )
        return msg.id

    def get_last_n_messages(self, n=10):
        return reversed(Message.objects.filter(group_name=self.room_group_name)[:n])

    def message_to_json(self, message):
        return {
            'message_id': message.id,
            'creator': message.creator.email,
            'content': message.content,
            'group_name': message.group_name,
            'created_at': message.created_at.isoformat()
        }
