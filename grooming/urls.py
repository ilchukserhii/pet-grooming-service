from django.urls import path

from grooming.views import (
    IndexView,
    ServiceListView,
    GroomerListView,
    CabinetView,
    ClientUpdateView,
    ClientPetCreateView,
    ClientPetDeleteView,
    ClientAppointmentCreateView,
    ClientAppointmentDeleteView,
    ClientAppointmentUpdateView,
    ClientCreateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("groomers/", GroomerListView.as_view(), name="groomer-list"),
    path("create_user/", ClientCreateView.as_view(), name="create-user"),
    path("cabinet/", CabinetView.as_view(), name="cabinet"),
    path("cabinet/update/", ClientUpdateView.as_view(), name="cabinet-update"),
    path(
        "cabinet/add_pet/",
        ClientPetCreateView.as_view(),
        name="cabinet-add-pet"
    ),
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
    path(
        "cabinet/appointments/<int:pk>/delete/",
        ClientAppointmentDeleteView.as_view(),
        name="cabinet-delete-appointment"
    ),
    path(
        "cabinet/appointments/<int:pk>/update/",
        ClientAppointmentUpdateView.as_view(),
        name="cabinet-update-appointment"
    )
]


app_name = "grooming"
