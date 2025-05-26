# core/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from core.views import responses

class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_token = self.scope['url_route']['kwargs']['token']
        self.group_name = f"client_{self.client_token}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print(f"Cliente {self.client_token} conectado.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Cliente {self.client_token} desconectado.")

    async def proxy_request(self, event):
        request_data = event['request_data']

        # Envia a requisição para o cliente via WebSocket
        await self.send(text_data=json.dumps({
            "action": "proxy_request",
            "request": request_data
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "proxy_response":
            response_data = data.get("response", {})

            # Espera que venha o request_id para mapear resposta correta
            request_id = response_data.get("request_id")
            if request_id:
                # Salva a resposta para ser lida pela view HTTP
                responses[request_id] = {
                    "status": response_data.get("status", 200),
                    "content": response_data.get("content", ""),
                }