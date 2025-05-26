from django.urls import path
from .views import proxy_view
from django.urls import path, re_path
from core import views

urlpatterns = [
    # rota para capturar o cliente e o path depois de /client/
    #re_path(r'^client/(?P<cliente>\w+)(?:/(?P<path>.*))?$', views.tunnel_view),

    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
]