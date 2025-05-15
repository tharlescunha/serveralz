from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tunel/(?P<client_id>\w+)/$', consumers.TunelConsumer.as_asgi()),
]