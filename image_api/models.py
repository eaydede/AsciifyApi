from django.db import models


class ImageData(models.Model):
    name = models.CharField(max_length=255, blank=True, null=False)
    path = models.CharField(max_length=255, default="images/", null=False)
    desc = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
