from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from image_api.models import Image
from image_api.serializers import ImageSerializer


class ImageView(CreateAPIView, ListAPIView, RetrieveAPIView):
    serializer = ImageSerializer
    querytset = Image.objects.all()

    def create(self, request, *args, **kwargs):
        return Response("Create", HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response("List", HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response("Retrieve", HTTP_200_OK)

@api_view(["GET"])
def image_list(request):
    return Response("List", HTTP_200_OK)