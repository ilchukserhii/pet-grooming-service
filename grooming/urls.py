from django.urls import path

from grooming.views import (
    index,
    ServiceListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
]


app_name = "grooming"