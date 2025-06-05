import asyncio
import websockets
import json
import pika

# Configuração do broker AMQP
broker_url = 'amqp://root:root@172.31.156.214:5672/%2F'

# Conexão pika (AMQP)
params = pika.URLParameters(broker_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
queue_name = 'proxy_requests'
channel.queue_declare(queue=queue_name, durable=True)

async def client_loop():
    uri = "wss://serveralz.azurewebsites.net/ws/client/cliente_1/"
    async with websockets.connect(uri) as websocket:
        print("Conectado como cliente_1")

        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data.get("action") == "proxy_request":
                request_data = data.get("request", {})
                request_id = request_data.get("request_id")

                try:
                    # Publica no broker AMQP
                    channel.basic_publish(
                        exchange='',
                        routing_key=queue_name,
                        body=json.dumps(request_data),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                        )
                    )
                    status = 200
                    content = f"Request enviada para fila {queue_name}"
                except Exception as e:
                    content = f"Erro ao enviar AMQP: {str(e)}"
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
