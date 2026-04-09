from django.urls import path

from grooming.views import (
    index,
    ServiceListView,
    GroomerListView,
    CabinetView,
    ClientUpdateView, ClientPetCreateView, ClientPetDeleteView, ClientAppointmentCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("groomers/", GroomerListView.as_view(), name="groomer-list"),
    path("cabinet/", CabinetView.as_view(), name="cabinet"),
    path("cabinet/update/", ClientUpdateView.as_view(), name="cabinet-update"),
    path("cabinet/add_pet/", ClientPetCreateView.as_view(), name="cabinet-add-pet"),
    path(
        "cabinet/pets/<int:pk>/delete_pet/",
        ClientPetDeleteView.as_view(),
        name="cabinet-delete-pet"
    ),
    path(
        "cabinet/create_appointment/",
        ClientAppointmentCreateView.as_view(),
        name="cabinet-create-appointment"
    ),
]


app_name = "grooming"
