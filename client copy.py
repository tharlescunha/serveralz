# client.py
import asyncio
import websockets
import json
import requests

async def client_loop():
    uri = "ws://127.0.0.1:8000/ws/client/cliente_1/"
    async with websockets.connect(uri) as websocket:
        print("Conectado como cliente_1")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data.get("action") == "proxy_request":
                request_data = data.get("request", {})
                request_id = request_data.get("request_id")
                path = request_data.get("path")
                url_local = f"http://localhost:8000{path}"

                try:
                    response = requests.get(url_local)
                    content = response.text
                    status = response.status_code
                except Exception as e:
                    content = f"Erro local: {str(e)}"
                    status = 500

                response_msg = {
                    "action": "proxy_response",
                    "response": {
                        "request_id": request_id,
                        "status": status,
                        "content": content,
                    }
                }
                await websocket.send(json.dumps(response_msg))

asyncio.run(client_loop())
