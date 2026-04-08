from django.urls import path

from grooming.views import (
    index,
    ServiceListView,
    GroomerListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("groomers/", GroomerListView.as_view(), name="groomer-list"),
]


app_name = "grooming"