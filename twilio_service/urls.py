from django.urls import path
from .views import TwilioWebhook

urlpatterns = [
    path('incoming-message/', TwilioWebhook.as_view(), name='income-message'),
]
