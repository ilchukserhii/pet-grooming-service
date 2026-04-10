from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from grooming.models import Service, Groomer, Pet


class PublicAccessViewTests(TestCase):
    def test_login_required_cabinet(self):
        response = self.client.get(reverse("grooming:cabinet"))
        self.assertRedirects(response, "/accounts/login/?next=/cabinet/")


class PrivateAccessViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_client = get_user_model().objects.create(
            phone_number="0501234567",
            first_name="Test",
            last_name="Test1",
            password="test12345",
        )
        cls.pet = Pet.objects.create(
            client=cls.test_client,
            name="Test_dog",
            pet_type="dog",
            breed="Big Dog",
        )
        cls.service = Service.objects.create(
            type="Test_service",
            price=10.00,
        )
        cls.groomer = Groomer.objects.create(
            first_name="Groomer",
            last_name="Test_Groomer",
        )
        cls.groomer.service.add(cls.service)

    def setUp(self):
        self.client.force_login(self.test_client)

    def test_login_required_cabinet(self):
        response = self.client.get(reverse("grooming:cabinet"))
        self.assertEqual(response.status_code, 200)

    def test_personal_data_view(self):
        response = self.client.get(reverse("grooming:cabinet"))
        self.assertIn(self.test_client.first_name, response.context["client"].first_name)
        self.assertIn(self.test_client.last_name, response.context["client"].last_name)
        self.assertIn(self.test_client.phone_number, response.context["client"].phone_number)
        self.assertIn(self.pet, response.context["pets"])

    def test_add_pet_for_client(self):
        response = self.client.post(
            reverse("grooming:cabinet-add-pet"),
            {
                "name": "Пусичька",
                "pet_type": "cat",
                "breed": "Какойто кот",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pet.objects.filter(name="Пусичька").exists())

    def test_delete_pet_for_client(self):
        pet = Pet.objects.create(
            client=self.test_client,
            name="На удаление",
            pet_type="dog",
            breed="Test",
        )
        response = self.client.post(
            reverse("grooming:cabinet-delete-pet", args=[pet.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pet.objects.filter(id=pet.id).exists())

    def test_other_client_delete_pet(self):
        other_client = get_user_model().objects.create(
            phone_number="0999999999",
            password="testpass9999",
        )
        pet = Pet.objects.create(
            client=other_client,
            name="На удаление",
            pet_type="dog",
            breed="Test",
        )
        response = self.client.post(
            reverse("grooming:cabinet-delete-pet", args=[pet.id]),
        )
        self.assertEqual(response.status_code, 404)



class SearchViewTests(TestCase):
    def test_search_services(self):
        service1 = Service.objects.create(
            type="Test1",
            price=10.00
        )
        service2 = Service.objects.create(
            type="Test2",
            price=10.00
        )
        response = self.client.get(
            reverse("grooming:service-list"),
            {"search": "Test1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(service1, response.context["services"])
        self.assertNotIn(service2, response.context["services"])

    def test_search_groomers(self):
        service = Service.objects.create(
            type="Test1",
            price=10.00
        )
        groomer1 = Groomer.objects.create(
            first_name="Test1",
            last_name="Test2",
        )
        groomer1.service.add(service)
        groomer2 = Groomer.objects.create(
            first_name="Test3",
            last_name="Test4",
        )
        groomer2.service.add(service)
        response = self.client.get(
            reverse("grooming:groomer-list"),
            {"search": "Test1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(groomer1, response.context["groomers"])
        self.assertNotIn(groomer2, response.context["groomers"])

