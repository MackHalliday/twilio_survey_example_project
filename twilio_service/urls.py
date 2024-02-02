from django.urls import path

from .webhook.views import TwilioWebhook
from .websocket.consumers import TwilioWebsocket

urlpatterns = [
    path("webhook-survey/", TwilioWebhook.as_view(), name="webhook-survey"),
    path("websocket-survey/", TwilioWebsocket().as_asgi(), name="websocket-survey"),
]
