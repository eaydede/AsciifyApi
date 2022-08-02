import os

from rest_framework import serializers

from image_api.models import ImageData


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageData
        fields = ['id', 'name', 'path', 'desc', 'created_at']
