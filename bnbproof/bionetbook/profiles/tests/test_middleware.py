from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from profiles.models import Profile


class ProfileMiddlewareTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )
            
    def test_my_profile_existence(self):
        
        self.assertTrue(self.client.login(username='testuser', password='password'))
        url = reverse("dashboard")
        
        response = self.client.get(url, follow=True)
        self.assertContains(response, "Please fill out your profile.")