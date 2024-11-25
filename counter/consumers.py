import json
from channels.generic.websocket import AsyncWebsocketConsumer

# For handling the WebSocket communications

class CounterConsumer(AsyncWebsocketConsumer):

    # To connect to the group
    async def connect(self):
        self.group_name = 'counter_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    # To disconnect from the group
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # To update the value of count when the value change
    async def send_counter_update(self, event):
        counter_value = event['value']
        print(f"Sending counter update: {counter_value}")
        await self.send(text_data=json.dumps({'value': counter_value}))
