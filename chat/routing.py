from django.urls import re_path
from . import counsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<username>\w+)/$",counsumer.ChatConsumer.as_asgi()),
]