from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from grooming.models import Groomer, Pet, Service, Appointment, Client


@admin.register(Client)
class ClientAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("first_name", "last_name",),
            }
        ),
        (
            "Advanced options",
            {
                "fields": ("email",),
            }
        )
    )


@admin.register(Groomer)
class GroomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name",]
    list_filter = ["service"]
    search_fields = ["first_name", "last_name"]


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "pet_type", "breed"]
    list_filter = ["pet_type"]
    search_fields = ["name", "breed"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["type", "price"]
    search_fields = ["type",]
    list_filter = ["price"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["date_time", "groomer", "pet"]
    list_filter = ["date_time"]
    search_fields = ["groomer__first_name", "groomer__last_name", "pet__name"]

