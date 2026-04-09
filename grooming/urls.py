from django.urls import path

from grooming.views import (
    index,
    ServiceListView,
    GroomerListView,
    CabinetView,
    ClientUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("groomers/", GroomerListView.as_view(), name="groomer-list"),
    path("cabinet/", CabinetView.as_view(), name="cabinet"),
    path("cabinet/update/", ClientUpdateView.as_view(), name="cabinet-update"),
]


app_name = "grooming"
