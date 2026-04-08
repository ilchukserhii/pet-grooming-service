from django.contrib.auth.models import AbstractUser
from django.db import models

from pet_grooming_service import settings


class Client(AbstractUser):

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    class PetType(models.TextChoices):
        DOG = "dog", "Собака"
        CAT = "cat", "Кіт"
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets"
    )
    name = models.CharField(max_length=100)
    pet_type = models.CharField(
        max_length=10,
        choices=PetType.choices,
    )
    breed = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.breed}) from client {self.client.first_name}"


class Groomer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    service = models.ManyToManyField("Service")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    type = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.type


class Appointment(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    groomer = models.ForeignKey(
        Groomer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appointments"
    )
    service = models.ManyToManyField(
        "Service",
        related_name="appointments"
    )
    date_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        groomer_name = (
            f"{self.groomer.first_name} {self.groomer.last_name}"
            if self.groomer else "No groomer"
        )
        return (
            f"{self.pet.name} "
            f"with {groomer_name} "
            f"at {self.date_time.strftime('%Y-%m-%d %H:%M')}"
        )

