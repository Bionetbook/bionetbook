from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
# from steps.models import Step
from organization.models import Organization, Membership


class ProtocolViewTests(TestCase):

    def setUp(self):

        # USER SETUP
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )

        # USER PROFILE SETUP
        self.profile = Profile.objects.create(
            user=self.user
        )

        # CREATE THE ORGANIZATION
        self.org = Organization.objects.create(name="testorg")
        self.org.save()

        # ADD THE MEMBERSHIP
        m = Membership(user=self.user, org=self.org)
        m.save()


        # CREATE PROTOCOL
        self.protocol = Protocol.objects.create(
            name = "Test Protocol",
            owner = self.org
        )

        self.protocol.save()
        # self.step = Step.objects.create(
        #     name = "Test Step",
        #     protocol=self.protocol
        # )
        # self.step.save()


    def test_create_protocol(self):

        url = reverse("protocol_create", kwargs={'owner_slug': self.org.slug})
        self.assertTrue(self.client.login(username='testuser', password='password'))
        
        data = dict(name="Test Protoco 2l", raw="blag nlag")
        response = self.client.post(url, data, follows=True)
        
    # def test_protocol_detail(self):        
    #     self.assertTrue(self.client.login(username='testuser', password='password'))
    #     url = self.protocol.get_absolute_url()
    #     response = self.client.get(url)
    #     self.assertContains(response, '<td><a href="/protocols/test-protocol/steps/test-step/">Test Step</a></td>')
        
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
