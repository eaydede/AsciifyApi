import json
import os

from django.test import TestCase, override_settings

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from image_api.asciify import asciify_image
from image_api.models import ImageData

from unittest import skip
from PIL import Image
from PIL import ImageChops

# Create your tests here.
class ImageListCreateTests(TestCase):
    cwd = os.path.dirname(__file__)
    data1 = {
        "name": "test1",
        "path": "{cwd}/images/test_image.png".format(cwd=cwd),
        "desc": "test description1",
    }
    data2 = {
        "name": "test2",
        "path": "{cwd}/images/test_image.png".format(cwd=cwd),
        "desc": "test description2",
    }

    def setUp(self):
        self.client = APIClient()

    def test_list_images(self):
        # Setup
        image_data1 = ImageData(**self.data1)
        image_data1.save()
        image_data2 = ImageData(**self.data2)
        image_data2.save()

        # Action
        response = self.client.get("/images/")
        parsed_response_content = json.loads(response.content)

        # Assertion
        self.assertIs(len(parsed_response_content), 2)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(parsed_response_content[0]["name"], self.data1["name"])
        self.assertEqual(parsed_response_content[0]["path"], self.data1["path"])
        self.assertEqual(parsed_response_content[0]["desc"], self.data1["desc"])
        self.assertEqual(parsed_response_content[1]["name"], self.data2["name"])
        self.assertEqual(parsed_response_content[1]["path"], self.data2["path"])
        self.assertEqual(parsed_response_content[1]["desc"], self.data2["desc"])

    @override_settings(MEDIA_ROOT=os.path.dirname(__file__))
    def test_post_image_with_image(self):
        # Setup
        with open("{cwd}/images/test_image.png".format(cwd=self.cwd), "rb") as image:
            # Action
            response = self.client.post("/images/", {"image": image, **self.data1})

        parsed_response_content = json.loads(response.content)

        # Assertion
        image_data = ImageData.objects.all()
        self.assertIs(image_data.count(), 1)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(parsed_response_content, image_data[0].id)

        original_image = Image.open("{cwd}/images/test_image.png".format(cwd=self.cwd))
        with Image.open(image_data[0].path) as saved_image:
            difference = ImageChops.difference(original_image, saved_image)

        # Checking to see that the images have no differences
        self.assertIs(difference.getbbox(), None)

    def test_post_image_without_image(self):
        # Setup
        with open("{cwd}/images/test_image.png".format(cwd=self.cwd), "rb") as image:
            # Action
            response = self.client.post("/images/")

        parsed_response_content = json.loads(response.content)

        # Assertion
        image_data = ImageData.objects.all()
        self.assertIs(image_data.count(), 0)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            parsed_response_content,
            "Please provide an image in the body of the request in the format of formdata",
        )

    def tearDown(self):
        # Make sure to remove all test files at the end of tests
        files_in_cwd = os.listdir(self.cwd)
        for file in files_in_cwd:
            if file.endswith(".PNG"):
                os.remove(os.path.join(self.cwd, file))


class ImageDetailTests(TestCase):
    cwd = os.path.dirname(__file__)
    data1 = {
        "name": "test1",
        "path": "{cwd}/images/test_image.png".format(cwd=cwd),
        "desc": "test description1",
    }

    def setUp(self):
        self.client = APIClient()

        self.image_data1 = ImageData(**self.data1)
        self.image_data1.save()

    def test_get_asciified_image(self):
        # Setup
        asciified_image = asciify_image(
            "{cwd}/images/test_image.png".format(cwd=self.cwd)
        )

        # Action
        response = self.client.get(
            "/images/{id}/".format(id=self.image_data1.id), format="text/plain"
        )

        # Assert
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEquals(json.loads(response.content), asciified_image)

    def test_get_asciified_image_invalid_id(self):
        # Action
        response = self.client.get("/images/{id}/".format(id=999), format="text/plain")

        # Assert
        self.assertEquals(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEquals(json.loads(response.content), "No image with given id")
