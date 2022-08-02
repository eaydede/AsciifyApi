from django.db import models


def upload_image_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


def upload_ascii_image_to(instance, filename):
    return 'ascii_images/{filename}'.format(filename=filename)


class ImageData(models.Model):
    name = models.CharField(max_length=255, null=False)
    path = models.CharField(max_length=255, null=False)
    desc = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)