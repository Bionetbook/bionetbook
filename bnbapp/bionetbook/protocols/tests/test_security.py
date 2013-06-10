# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.test import TestCase

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
from protocols.tests.core import AutoBaseTest
# from steps.models import Step
from organization.models import Organization, Membership


class ProtocolSecurityTests(AutoBaseTest):

    def setUp(self):
        super(ProtocolSecurityTests, self).setUp()

        # USER SETUP
        self.user = self.createUserInstance(username="testuser", password="pass", email="test@example.com")
        self.userTwo = self.createUserInstance(username="usertwo", password="pass", email="usertwo@example.com")

        # USER PROFILE SETUP
        self.profile = self.createModelInstance(Profile, user=self.user)
        self.profileTwo = self.createModelInstance(Profile, user=self.userTwo)

        # CREATE THE ORGANIZATION
        self.org = self.createModelInstance(Organization, name="TestOrg")
        self.orgTwo = self.createModelInstance(Organization, name="TestTwoOrg")

        # ADD THE MEMBERSHIP
        self.member = self.createModelInstance(Membership, user=self.user, org=self.org)
        self.memberTwo = self.createModelInstance(Membership, user=self.userTwo, org=self.orgTwo)

        # CREATE PROTOCOL
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org)

    def test_login(self):
        url = reverse("protocol_create", kwargs={'owner_slug': self.org.slug})
        self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.user is the first user

    # def test_user_has_access(self):
    #     url = reverse("protocol_create", kwargs={'owner_slug': self.org.slug})
    #     self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.user is the first user

    # def test_user_has_no_access(self):
    #     url = reverse("protocol_create", kwargs={'owner_slug': self.org.slug})
    #     self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.user is the first user
