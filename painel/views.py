from django.http import JsonResponse, HttpResponseNotFound
from .consumers import CLIENTES_CONECTADOS
from asgiref.sync import async_to_sync

async def redireciona_para_cliente(request, client_id):
    consumer = CLIENTES_CONECTADOS.get(client_id)

    if consumer:
        mensagem = f"Nova requisição: {request.method} {request.path}"
        await consumer.send(text_data=mensagem)
        return JsonResponse({"status": "mensagem enviada para o cliente"})
    else:
        return HttpResponseNotFound("Cliente não conectado")
    
def lista_clientes_conectados(request):
    return JsonResponse({
        "clientes_conectados": list(CLIENTES_CONECTADOS.keys())
    })
