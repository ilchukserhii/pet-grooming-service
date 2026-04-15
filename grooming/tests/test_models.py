import datetime

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from grooming.models import Pet, Groomer, Service, Appointment


class ClientModelTest(TestCase):
    def test_client_username_equal_phone_number(self):
        client = get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
        )
        self.assertEqual(client.username, "0501234567")

    def test_client_str(self):
        client = get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
            first_name="Test",
            last_name="Test1",
        )
        self.assertEqual(
            str(client), f"{client.first_name} {client.last_name}"
        )

    def test_client_phone_number_unique(self):
        get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
        )
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create(
                phone_number="0501234567",
                password="test123",
            )


class PetModelTest(TestCase):
    def test_pet_str(self):
        client = get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
        )
        pet = Pet.objects.create(
            client=client,
            name="Test",
            pet_type=Pet.PetType.DOG,
            breed="Test",
        )
        self.assertEqual(
            str(pet),
            f"{pet.name} ({pet.breed}) - клієнт {pet.client.first_name}"
        )


class GroomerModelTest(TestCase):
    def test_groomer_str(self):
        service = Service.objects.create(
            type="Стрижка",
            price=10.00,
        )
        groomer = Groomer.objects.create(
            first_name="Test",
            last_name="Test",
        )
        groomer.service.add(service)
        self.assertEqual(
            str(groomer),
            f"{groomer.first_name} {groomer.last_name}"
        )


class AppointmentModelTest(TestCase):
    def test_appointment_str(self):
        client = get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
        )
        pet = Pet.objects.create(
            client=client,
            name="Test",
            pet_type=Pet.PetType.DOG,
            breed="Test",
        )
        service = Service.objects.create(
            type="Стрижка",
            price=10.00,
        )
        appointment = Appointment.objects.create(
            pet=pet,
            date_time=datetime.date.today(),
        )
        appointment.service.add(service)
        self.assertEqual(
            str(appointment),
            f"{appointment.pet.name} "
            f"with No groomer "
            f"at {appointment.date_time.strftime('%Y-%m-%d %H:%M')}"
        )