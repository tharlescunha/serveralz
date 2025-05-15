import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Dicionário global para armazenar conexões
CLIENTES_CONECTADOS = {}

class TunelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        CLIENTES_CONECTADOS[self.client_id] = self
        await self.accept()

    async def disconnect(self, close_code):
        CLIENTES_CONECTADOS.pop(self.client_id, None)

    async def receive(self, text_data):
        # Aqui você pode tratar mensagens vindas do client
        print(f"[{self.client_id}] ➡️ {text_data}")