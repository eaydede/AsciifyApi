from django.contrib import admin
from django.urls import path, include

from image_api.views import ImageListCreateView, ImageDetailView

urlpatterns = [
    path("", ImageListCreateView.as_view(), name="image_list"),
    path("", ImageListCreateView.as_view(), name="image_create"),
    path("<int:id>/", ImageDetailView.as_view(), name="image_detail"),
]
