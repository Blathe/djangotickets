from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class TicketTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="test_password", email="test@test.com")
        self.user = User.objects.get(pk=1)

    def test_valid_user(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "test_user")

    def test_create_ticket_without_being_authenticated(self):
        ticket = {
            "title":"Test",
            "description":"test description",
            "priority": 2,
            "status": "OPEN",
        }
        resp = self.client.post(reverse("create"), ticket)
        self.assertEquals(resp.status_code, 302)
        self.client.force_login(self.user)
        resp = self.client.post(reverse("create"), ticket)
        self.assertEquals(resp.status_code, 200)
