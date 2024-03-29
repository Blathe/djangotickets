from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class TicketTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password", email="test@test.com")

    def test_user_exists(self):
        self.user = User.objects.get(pk=1)
        self.assertEqual(self.user.username, "test_user")
        
    def test_create_ticket_without_being_authenticated(self):
        """This test should pass if a user receives a response status code of 302 before being authenticated when trying to create a ticket
        and a status of 200 after being authenticated when trying to create another ticket.
        """
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
        
    def test_create_ticket_with_invalid_priority(self):
        """This should pass if the response status code is 302 (the Create view returns a status 302 due to redirect if ticket validation fails)
        when we post an invalid ticket. We should get a status 200 when posting a valid ticket.
        """
        invalid_ticket = {
            "title":"Test",
            "description":"test description",
            "priority": 'INVALID_PRIORITY',
            "status": "OPEN",
        }
        self.client.force_login(self.user)
        resp = self.client.post(reverse("create"), invalid_ticket)
        self.assertEquals(resp.status_code, 302)
        valid_ticket = {
            "title":"Test",
            "description":"test description",
            "priority": 1,
            "status": "OPEN",
        }
        resp = self.client.post(reverse("create"), valid_ticket)
        self.assertEquals(resp.status_code, 200)