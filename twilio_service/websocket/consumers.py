import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TwilioWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect")
        pass

    async def receive(self, text_data):
        print("recieve")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))
