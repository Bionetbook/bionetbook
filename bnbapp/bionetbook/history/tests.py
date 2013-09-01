"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
1. catch change in protocol keys
2. catch added step 
3. catch removed step 
4. catch edited step 
5. catch edited step children 
6. catch added action 
7. catch removed action 
8. catch edited action 
9. catch edited step action 
10. catch added child 
11. catch removed child
12. catch edited child 
"""

from django.test import TestCase
from core.tests import AutoBaseTest

class SimpleTest(TestCase):
    def test_added_step(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)



class ProtocolModelTests(AutoBaseTest):

    def setUp(self):
        super(ProtocolModelTests, self).setUp()
        self.protocol = None
        self.user = self.createUserInstance( username="testuser", password="password", email="test@example.com" )        # CREATE THE USER
        self.org = self.createModelInstance(Organization, name="testorg")        # CREATE THE ORGANIZATION
        self.membership = self.createModelInstance(Membership, user=self.user, org=self.org)        # ADD THE MEMBERSHIP

    def test_catch_change_in_protocol_values(self):
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")
        self.protocol.save()

        # CHECK THE CHANGES HERE IN THE PROTOCOL

        # self.assertEquals(self.protocol.raw, "what?")
        # self.assertEquals(self.protocol.slug, "%d-test-protocol" % self.protocol.pk)
