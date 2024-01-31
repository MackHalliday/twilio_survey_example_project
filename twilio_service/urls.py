from django.urls import path

from .webhook.views import TwilioWebhook
from .websocket.consumers import TwilioConsumer

urlpatterns = [
    path("webhook/survey/", TwilioWebhook.as_view(), name="webhook-survey"),
    path("websocket/survey/", TwilioConsumer().as_asgi(), name="websocket-survey"),
]
