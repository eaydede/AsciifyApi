from django.db import models


def upload_image_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


def upload_ascii_image_to(instance, filename):
    return 'ascii_images/{filename}'.format(filename=filename)


class Image(models.Model):
    image = models.ImageField(upload_to=upload_image_to, null=False)
    ascii_image = models.FileField(upload_to=upload_ascii_image_to, blank=True, null=True)
