import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import painel.routing  # Ajuste pro seu app que tem o websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servidor_tunel.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Tratamento normal HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            painel.routing.websocket_urlpatterns  # Aqui suas rotas websocket
        )
    ),
})
