from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
# from steps.models import Step
from organization.models import Organization


class ProtocolViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.organization = Organization.objects.create(name="testorg")
        self.protocol = Protocol.objects.create(
            name = "Test Protocol",
            owner = self.organization
        )
        self.protocol.save()
        # self.step = Step.objects.create(
        #     name = "Test Step",
        #     protocol=self.protocol
        # )
        # self.step.save()


    def test_create_protocol(self):

        url = reverse("protocol_create", kwargs={'owner_slug': self.organization.slug})
        self.assertTrue(self.client.login(username='testuser', password='password'))
        
        data = dict(name="Test Protoco 2l", raw="blag nlag")
        response = self.client.post(url, data, follows=True)
        
    # def test_protocol_detail(self):
        
    #     self.assertTrue(self.client.login(username='testuser', password='password'))
    #     url = self.protocol.get_absolute_url()
    #     response = self.client.get(url)
    #     self.assertContains(response, '<td><a href="/protocols/test-protocol/steps/test-step/">Test Step</a></td>')
        
        
