from uuid import uuid4

from django.conf import settings
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
        data = request.data
        # If file cannot be opened then an image has not been provided in the request body
        try:
            image = PILImage.open(request.FILES['image'])
        except MultiValueDictKeyError:
            return Response(
                data='Please provide an image in the body of the request in the format of formdata',
                status=HTTP_400_BAD_REQUEST
            )
        
        # Generate a unique actual name for the image being stored so as
        # to avoid collisions with duplicate image names
        data['path'] = '{image_folder}/{unique_name}.{format}'.format(
            image_folder=settings.MEDIA_ROOT,
            unique_name=str(uuid4().hex[:6].upper()),
            format=image.format
        )

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # Save new image_data instance after any validation
            image_data = serializer.save()
            # Save the image in the given path
            image.save(fp=image_data.path, format=image.format)

            return Response(image_data.id, HTTP_201_CREATED)

        # Return any errors that occured during serialization
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

        # Check to see if image_data instance with provided id exists
        try:
            image_data = ImageData.objects.get(pk=image_id)
        except ObjectDoesNotExist:
            return Response('No image with given id', HTTP_400_BAD_REQUEST)

        # Asciify the image and return it in the response body as plain text
        asciified_image = asciify_image(img_path=image_data.path)
        # NOTE: Having trouble with the ascii image's '\n' character not being interpreted as
        # a new line so editing the size of the terminal window is required.
        return Response(data=asciified_image, status=HTTP_200_OK, content_type='text/plain')