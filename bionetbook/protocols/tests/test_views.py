from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from protocols.models import Protocol


class ProtocolViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )

    def test_create_protocol(self):

        url = reverse("protocol_create")
        self.assertTrue(self.client.login(username='testuser', password='password'))
        
        data = dict(name="test-protocol", raw="blag nlag")
        response = self.client.post(url, data, follows=True)
        print response
