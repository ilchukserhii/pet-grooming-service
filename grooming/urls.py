from django.urls import path

from grooming.views import (
    index
)

urlpatterns = [
    path("", index, name="index"),
]


app_name = "grooming"