from django.urls import path
from . import views

urlpatterns = [
    path('sms/webhook/', views.sms_webhook, name='sms_webhook'),
]
