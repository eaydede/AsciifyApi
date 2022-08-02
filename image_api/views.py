from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from PIL import Image as PILImage

from image_api.models import ImageData
from image_api.serializers import ImageSerializer

from image_api.asciify import asciify_image


class ImageListCreateView(APIView):
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        # Create initial data object to be filled by request and used by serializer
        data = {
            'name': '',
            'path': 'images/',
            'desc': ''
        }
        # If file cannot be opened then an image has not been provided in the request body
        try:
            image = PILImage.open(request.FILES['image'])
        except MultiValueDictKeyError:
            return Response('Please provide an image in the body of the request in the format of formdata')
        if request.data['name']:
            data['name'] = request.data['name'] + '.' + image.format
        else:
            data['name'] = str(uuid4().hex[:6].upper()) + "." + image.format

        data['path'] = data['path'] + data['name']

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            image_data = serializer.save()
            image.save(fp=data['path'], format=image.format)

            return Response(image_data.id, HTTP_201_CREATED)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        # Get all image data objects
        result = ImageData.objects.all()
        # Serialize the result
        serialized_result = self.serializer_class(result, many=True)
        # Return serialized list in response
        return Response(serialized_result.data, HTTP_200_OK)


class ImageDetailView(APIView):
    serializer_class = ImageSerializer

    def get(self, request, *args, **kwargs):
        image_id = kwargs['id']
        try:
            image_data = ImageData.objects.get(pk=image_id)
        except ObjectDoesNotExist:
            return Response('No image with given id', HTTP_200_OK)

        asciified_image = asciify_image(img_path=image_data.path)
        return Response(asciified_image, HTTP_200_OK, content_type="text/plain")