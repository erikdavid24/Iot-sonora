import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unirse al grupo "sensores"
        await self.channel_layer.group_add("sensores", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard("sensores", self.channel_name)

    # Este método se llama cuando el MQTT manda un dato al grupo
    async def sensor_update(self, event):
        data = event['data']
        # Enviar dato al Frontend (Javascript)
        await self.send(text_data=json.dumps(data))