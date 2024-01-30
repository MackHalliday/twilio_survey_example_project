from audioop import reverse

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class OptOutAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "opt_out.html")

    def post(self, request: HttpRequest) -> Response:
        return Response(
            data={"message": "Opt-out request processed"}, status=status.HTTP_200_OK
        )
