import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import MyModel


class MyModelConsumer(WebsocketConsumer):
    def connect(self):
        self.object_id = self.scope["url_route"]["kwargs"]["object_id"]
        self.room_group_name = f"object_{self.object_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        if MyModel.objects.filter(id=self.object_id).exists():
            self.accept()
            instance = MyModel.objects.get(id=self.object_id)
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "message", "instance": {"instance_id": instance.id}}
            )
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def message(self, event):
        instance_id = event["instance_id"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"instance_id": instance_id}))
