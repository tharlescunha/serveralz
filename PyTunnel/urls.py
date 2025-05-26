from django.contrib import admin
from django.urls import path, include
from core import views  # ajusta para o seu app/views.py
from django.urls import re_path

urlpatterns = [
    # rota para capturar /client/<cliente>/<qualquer coisa opcional>
    #re_path(r'^client/(?P<cliente>\w+)(?:/(?P<path>.*))?$', views.tunnel_view),
    re_path(r'^(?P<path>.*)$', views.tunnel_view),

    path('/', include('core.urls')),
    
    # suas outras rotas:
    path('admin/', admin.site.urls),
    path('wsproxy/<str:client_id>/<path:path>/', views.proxy_view),
    #re_path(r'^cliente_(?P<client_token>\w+)/(?P<path>.*)$', views.outro_view),
]