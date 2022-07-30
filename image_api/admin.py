from django.contrib import admin

from image_api.models import Image

# Register your models here.
@admin.register(Image)
class CourseModelAdmin(admin.ModelAdmin):
    pass