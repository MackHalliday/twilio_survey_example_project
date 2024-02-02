from django.urls import path

from .webhook.views import TwilioWebhook

urlpatterns = [
    path("webhook-survey/", TwilioWebhook.as_view(), name="webhook-survey"),
]
