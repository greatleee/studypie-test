from django.urls import re_path

from .consumers import AlarmConsumer

websocket_urlpatterns = [
    re_path(r'alarms/$', AlarmConsumer.as_asgi()),
]
