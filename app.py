import asyncio
import websockets
import requests
import json

async def cliente_tunel():
    uri = "wss://serveralz.azurewebsites.net/ws/cliente_1/"
    print("[CLIENTE] Conectando ao servidor...")

    async with websockets.connect(uri) as websocket:
        print("[CLIENTE] Conectado!")

        while True:
            msg = await websocket.recv()
            print(f"[CLIENTE] Mensagem recebida: {msg}")

            data = json.loads(msg)

            if data.get("acao") == "fazer_requisicao_local":
                url_local = data.get("url_local", "http://localhost:5000/")
                try:
                    resposta = requests.get(url_local)
                    await websocket.send(json.dumps({
                        "status": "ok",
                        "resposta": resposta.text
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "status": "erro",
                        "mensagem": str(e)
                    }))

asyncio.run(cliente_tunel())