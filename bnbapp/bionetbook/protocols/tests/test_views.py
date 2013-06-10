from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
# from steps.models import Step
from organization.models import Organization, Membership
from protocols.tests.core import AutoBaseTest


class ProtocolViewTests(AutoBaseTest):

    def setUp(self):
        super(ProtocolViewTests, self).setUp()

        self.user = self.createUserInstance(username="testuser", password="pass", email="test@example.com")        # USER SETUP
        self.profile = self.createModelInstance(Profile, user=self.user)        # USER PROFILE SETUP
        self.org = self.createModelInstance(Organization, name="TestOrg")        # CREATE THE ORGANIZATION
        self.member = self.createModelInstance(Membership, user=self.user, org=self.org)        # ADD THE MEMBERSHIP
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org)        # CREATE PROTOCOL

    def test_create_protocol(self):
        url = reverse("protocol_create", kwargs={'owner_slug': self.org.slug})
        self.assertTrue(self.client.login(username='testuser', password='pass'))
        
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
