from django.urls import path

from grooming.views import (
    index,
    ServiceListView,
    GroomerListView, CabinetView,
)

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("groomers/", GroomerListView.as_view(), name="groomer-list"),
    path("cabinet/", CabinetView.as_view(), name="cabinet"),
]


app_name = "grooming"