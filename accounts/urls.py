from django.urls import path

from . import views

urlpatterns = [
    path("opt-out/", views.OptOutAPIView.as_view(), name="opt-out"),
]
