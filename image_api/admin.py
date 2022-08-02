from django.contrib import admin

from image_api.models import ImageData

# Register your models here.
@admin.register(ImageData)
class CourseModelAdmin(admin.ModelAdmin):
    pass