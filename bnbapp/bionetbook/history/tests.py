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

import pprint
pp = pprint.PrettyPrinter(indent=4)

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
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?", author=self.user)

    def test_history_logging_for_protocol(self):
        history = self.protocol.history_set.all()
        self.assertEquals(len(history), 1)
        # print "TEST ONE"
        # pp.pprint( history[0].data )

        self.assertEquals(history[0].data['create'][0]['id'], 1)
        self.assertEquals(history[0].data['create'][0]['attrs']['name'], "Test Protocol")

    def test_catch_change_in_protocol_values(self):
        self.protocol.name = "New Test Protocol"
        self.protocol.save()

        history = self.protocol.history_set.all()
        self.assertEquals(len(history), 2)

        # for h in history:
        #     print "HISTORY ENTRY: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(history[0].data['update'][0]['id'], 1)
        self.assertEquals(history[0].data['update'][0]['attrs']['name'], "New Test Protocol")


    def test_catch_change_in_published_protocol_values(self):
        self.protocol.name = "New Published Protocol"
        self.protocol.published = True
        self.protocol.save()

        history = self.protocol.history_set.all()
        self.assertEquals(len(history), 2)

        for h in history:
            print "\nHISTORY ENTRY: %d" % h.pk
            pp.pprint( h.data )

        self.assertEquals(history[0].data['update'][0]['id'], 1)
        self.assertEquals(history[0].data['update'][0]['attrs']['name'], "New Published Protocol")


    # def test_catch_adding_step(self):
    #     pass
