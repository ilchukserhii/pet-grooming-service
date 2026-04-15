from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from grooming.models import GuestQuickRequest


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.test_client = get_user_model().objects.create_user(
            username="user",
            password="testclient",
            phone_number="0501234567",
        )

    def test_client_phone_number_listed(self):
        """
        Test that the client phone number is in list_display on admin page
        :return:
        """
        url = reverse("admin:grooming_client_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.test_client.phone_number)

    def test_client_detail_phone_number_listed(self):
        """
        Test that the client`s phone number is in client detail admin page
        :return:
        """
        url = reverse("admin:grooming_client_change", args=[self.test_client.pk])
        response = self.client.get(url)
        self.assertContains(response, self.test_client.phone_number)

    def test_client_add_page_fields(self):
        url = reverse("admin:grooming_client_add")
        response = self.client.get(url)
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "Email address:")
        self.assertContains(response, "Phone number:")

    def test_anonymous_user_redirected_to_login_page(self):
        anon_client = Client()
        url = reverse("admin:index")
        response = anon_client.get(url)
        self.assertRedirects(response, "/admin/login/?next=%s" % url)

    def test_guest_quick_request(self):
        self.quick_request = GuestQuickRequest.objects.create(
            name="Вася",
            phone_number="0501234567",
            pet_type=GuestQuickRequest.PetType.DOG,
            breed="Шибаину",
        )
        url = reverse("admin:grooming_guestquickrequest_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.quick_request.name)
        self.assertContains(response, self.quick_request.phone_number)
        self.assertContains(response, "Собака")
        self.assertContains(response, self.quick_request.breed)
        self.assertContains(response, self.quick_request.is_processed)