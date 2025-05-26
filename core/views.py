# views.py
from django.http import HttpResponse, HttpResponseNotFound
import asyncio
import json
import uuid
import asyncio
import json
from django.http import HttpResponse, JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import ConnectedClient

import secrets

from django.shortcuts import render, redirect
from .forms import ClienteForm

channel_layer = get_channel_layer()

from channels.layers import get_channel_layer

# variável global para guardar cliente ativo
CLIENTE_ATIVO = "cliente_1"  # Pode atualizar essa variável via websocket connect

responses = {}  # Ou importe do consumers.py

async def proxy_view(request, client_id, path):
    channel_layer = get_channel_layer()
    request_id = str(uuid.uuid4())

    # Envia via WebSocket para o client pedido do recurso
    message = {
        "type": "proxy_request",
        "request_id": request_id,
        "path": "/" + path,
        "method": request.method,
        # Pode enviar headers e body também, se quiser
    }

    # Envia para grupo do cliente
    await channel_layer.group_send(
        f"client_{client_id}",
        {
            "type": "proxy_request",
            "text": json.dumps(message),
        }
    )

    # Espera a resposta do cliente (timeout de 10 segundos)
    for i in range(100):
        if request_id in responses:
            resp = responses.pop(request_id)
            status = resp.get("status", 200)
            content = resp.get("content", "")
            return HttpResponse(content, status=status)
        await asyncio.sleep(0.1)

    return HttpResponseNotFound("Timeout: cliente não respondeu")


# Dicionário global para guardar respostas pendentes

#Para usar apenas com um clinte, foi colocado o clinte global 
#def tunnel_view(request, cliente, path=None):
def tunnel_view(request, path=None):
    cliente = CLIENTE_ATIVO  # usar o cliente fixo/ativo aqui
    request_data = {
        "method": request.method,
        "path": path,
        "headers": dict(request.headers),
        "body": request.body.decode("utf-8", errors="ignore"),
        "query_string": request.META.get("QUERY_STRING", ""),
    }

    request_id = str(uuid.uuid4())  # ID único para essa requisição

    async def send_and_receive():
        # Envia mensagem para o grupo do cliente
        await channel_layer.group_send(
            f"client_{cliente}",
            {
                "type": "proxy_request",
                "request_data": {**request_data, "request_id": request_id},
            },
        )

        # Aguarda resposta no dicionário responses, timeout 5 segundos
        for _ in range(50):
            if request_id in responses:
                response = responses.pop(request_id)
                return response
            await asyncio.sleep(0.1)

        return {"status": 504, "content": "Timeout: no response from client"}

    response_data = async_to_sync(send_and_receive)()

    return HttpResponse(
        response_data.get("content", ""), status=response_data.get("status", 500)
    )

def gerar_token():
    return secrets.token_hex(16)

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.token = gerar_token()
            cliente.save()
            return redirect('listar_clientes')  # ou mostrar o token
    else:
        form = ClienteForm()
    return render(request, 'cadastrar_cliente.html', {'form': form})

def listar_clientes(request):
    clientes = ConnectedClient.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})