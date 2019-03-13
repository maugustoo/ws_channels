""" Consumers for websocket"""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AlarmNotificationConsumer(WebsocketConsumer):
    """ Consumers for alarm notification websocket"""
    # pylint: disable=attribute-defined-outside-init
    def connect(self):
        """Join room group according the room name"""
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    # pylint: disable=unused-argument
    def disconnect(self, close_code):  # pylint: disable=arguments-differ
        """Leave room group according the room name"""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):  # pylint: disable=arguments-differ
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'alarm_notification',
                'message': message
            }
        )

    def alarm_notification(self, event):
        """Receive message from room group"""
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
