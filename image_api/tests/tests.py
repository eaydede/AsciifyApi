import json
import os

from django.test import TestCase, override_settings, Client

from rest_framework.test import APIClient

from asciify_service.settings import MEDIA_ROOT
from image_api.models import ImageData

from PIL import Image

# Create your tests here.
class ImageListCreateTests(TestCase):
    client = Client()
    cwd = os.path.dirname(__file__)
    data1 = {
        'name': 'test1',
        'path': '../images/test_image.png',
        'desc': "test description1"
    }
    data2 = {
        'name': 'test2',
        'path': '../images/test_image.png',
        'desc': "test description2"
    }

    def test_list_images(self):
        # Setup
        image_data1 = ImageData(**self.data1)
        image_data1.save()
        image_data2 = ImageData(**self.data2)
        image_data2.save()

        # Action
        response = self.client.get('/images/')
        parsed_response_content = json.loads(response.content)

        # Assertion
        self.assertIs(len(parsed_response_content), 2)
        self.assertEqual(parsed_response_content[0]['name'], self.data1['name'])
        self.assertEqual(parsed_response_content[0]['path'], self.data1['path'])
        self.assertEqual(parsed_response_content[0]['desc'], self.data1['desc'])
        self.assertEqual(parsed_response_content[1]['name'], self.data2['name'])
        self.assertEqual(parsed_response_content[1]['path'], self.data2['path'])
        self.assertEqual(parsed_response_content[1]['desc'], self.data2['desc'])

    @override_settings(MEDIA_ROOT=os.path.dirname(__file__))
    def test_post_image_with_image(self):
        # Setup
        with open('{cwd}/images/test_image.png'.format(cwd=self.cwd), 'rb') as image:
            # Action
            response = self.client.post('/images/', {'image': image, 'name': 'name'})
        
        parsed_response_content = json.loads(response.content)

        # Assertion
        print(parsed_response_content)

        # Teardown
        files_in_cwd = os.listdir(self.cwd)
        for file in files_in_cwd:
            if file.endswith('.PNG'):
                os.remove(os.path.join(self.cwd, file))

    def tearDown(self):
        pass