from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RecipeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("recipes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("recipes", self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            "recipes",
            {
                "type": "send_update",
                "message": text_data,
            }
        )

    async def send_update(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
