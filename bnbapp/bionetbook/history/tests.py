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

from protocols.models import Protocol, Action, Step, Component
from organization.models import Organization, Membership

# class SimpleTest(TestCase):
#     def test_added_step(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)



class HistoryModelTests(AutoBaseTest):

    def setUp(self):
        super(HistoryModelTests, self).setUp()
        self.protocol = None
        self.user = self.createUserInstance( username="testuser", password="password", email="test@example.com" )        # CREATE THE USER
        self.org = self.createModelInstance(Organization, name="testorg")        # CREATE THE ORGANIZATION
        self.membership = self.createModelInstance(Membership, user=self.user, org=self.org)        # ADD THE MEMBERSHIP
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")

    def test_history_logging_for_protocol(self):
        history = self.protocol.history_set.all()
        self.assertEquals(len(history), 1)
        print history[0].data


    def test_catch_change_in_protocol_values(self):
        self.protocol.name = "New Test Protocol"
        self.protocol.save()

        history = self.protocol.history_set.all()
        self.assertEquals(len(history), 2)
        print history[1].data
