import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CounterConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'counter_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_counter_update(self, event):
        counter_value = event['value']
        print(f"Sending counter update: {counter_value}")
        await self.send(text_data=json.dumps({'value': counter_value}))
