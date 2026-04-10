from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from grooming.models import (
    Groomer,
    Pet,
    Service,
    Appointment,
    Client,
    GuestQuickRequest
)


@admin.register(Client)
class ClientAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ("first_name", "last_name", "phone_number"),
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
    list_display = ["date_time", "groomer", "pet", "is_completed"]
    list_filter = ["date_time", "is_completed"]
    search_fields = ["groomer__first_name", "groomer__last_name", "pet__name"]


@admin.register(GuestQuickRequest)
class GuestQuickRequestAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone_number",
        "pet_type",
        "breed",
        "created_at",
        "is_processed"
    ]
    list_filter = ["created_at"]
    search_fields = ["name", "phone_number"]
