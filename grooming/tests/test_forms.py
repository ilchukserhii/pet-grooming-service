import datetime
from time import strptime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from grooming.forms import ClientCreateForm, ClientUpdateForm, ClientPetCreateForm, ClientAppointmentForm, GuestForm
from grooming.models import Pet, Service, Groomer


class ClientCreateFormTest(TestCase):
    def test_client_creation_form_valid(self):
        form_data = {
            "phone_number": "0501234567",
            "password1": "Strongpass123",
            "password2": "Strongpass123",
        }
        form = ClientCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_creation_form_invalid(self):
        form_data = {
            "password1": "Strongpass123",
            "password2": "Strongpass123",
        }
        form = ClientCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class ClientUpdateFormTest(TestCase):
    def test_client_update_form_valid(self):
        form_data = {
            "phone_number": "0501234567",
        }
        form = ClientUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_update_form_invalid(self):
        form_data = {
            "phone_number": "8501234567",
        }
        form = ClientUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class ClientClientPetFormTest(TestCase):
    def test_client_client_pet_form_valid(self):
        form_data = {
            "name": "Test",
            "pet_type": "dog",
            "breed": "Test",
        }
        form = ClientPetCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_client_pet_form_invalid(self):
        form_data = {}
        form = ClientPetCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class ClientAppointmentFormTest(TestCase):
    def setUp(self):
        self.test_client = get_user_model().objects.create(
            phone_number="0501234567",
            password="test123",
        )
        self.pet = Pet.objects.create(
            client=self.test_client,
            name="Test",
            pet_type=Pet.PetType.DOG,
            breed="Test",
        )
        self.service = Service.objects.create(
            type="test",
            price=10.00,
        )
        self.groomer = Groomer.objects.create(
            first_name="Test",
            last_name="Test",
        )
        self.groomer.service.add(self.service)

    def test_client_appointment_form_valid(self):
        form_data = {
            "pet": self.pet.id,
            "service": [self.service.id,],
            "groomer": self.groomer.id,
            "appointment_date": "2026-09-22",
            "appointment_time": "13:00",
        }
        form = ClientAppointmentForm(data=form_data)
        form.fields["pet"].queryset = Pet.objects.filter(client=self.test_client)
        self.assertTrue(form.is_valid())

    def test_client_appointment_form_invalid(self):
        form_data = {
            "pet": "",
            "service": [self.service.id,],
            "groomer": self.groomer.id,
            "appointment_date": "2026-09-22",
            "appointment_time": "13:00",
        }
        form = ClientAppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_client_form_invalid_date(self):
        form_data = {
            "pet": self.pet.id,
            "service": [self.service.id,],
            "groomer": self.groomer.id,
            "appointment_date": "2020-09-22",
            "appointment_time": "13:00"
        }
        form = ClientAppointmentForm(data=form_data)
        self.assertIn("Запис повинен бути на майбутнє", form.non_field_errors())


class GuestFormTest(TestCase):
    def test_guest_form_valid(self):
        form_data = {
            "phone_number": "0501234567",
            "name": "Test",
            "pet_type": "dog",
            "breed": "Test",
        }
        form = GuestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_guest_form_invalid_phone_number(self):
        form_data = {
            "phone_number": "8501234567",
            "name": "Test",
            "pet_type": "dog",
            "breed": "Test",
        }
        form = GuestForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_guest_form_invalid(self):
        form_data = {
            "phone_number": "0501234567",
            "name": "",
            "pet_type": "dog",
            "breed": "Test",
        }
        form = GuestForm(data=form_data)
        self.assertFalse(form.is_valid())
