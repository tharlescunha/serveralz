from django.urls import path
from .views import lista_clientes_conectados, redireciona_para_cliente

urlpatterns = [
    path("clientes/", lista_clientes_conectados, name="clientes_conectados"),
    path("<str:client_id>/", redireciona_para_cliente, name="redireciona_cliente"),
]