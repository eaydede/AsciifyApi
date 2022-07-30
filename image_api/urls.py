from django.contrib import admin
from django.urls import path, include

from image_api.views import ImageView

urlpatterns = [
    path('', ImageView.as_view(), name="image_list"),
    path('', ImageView.as_view(), name="image_create"),
    path('<int:id>', ImageView.as_view(), name="image_retrieve"),
]