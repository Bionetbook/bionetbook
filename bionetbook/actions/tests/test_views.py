from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from actions.models import Action


class ActionViewTests(TestCase):
    
    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )
            
        self.protocol = Protocol