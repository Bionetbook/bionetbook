from django.contrib.auth.models import User
from django.test import TestCase

# from actions.models import Action
from protocols.models import Protocol, Action, Step, Component
# from steps.models import Step
from organization.models import Organization, Membership
from protocols.tests.core import AutoBaseTest

class ProtocolModelTests(AutoBaseTest):

    def setUp(self):
        super(ProtocolModelTests, self).setUp()
        self.protocol = None
        self.user = self.createUserInstance( username="testuser", password="password", email="test@example.com" )        # CREATE THE USER
        self.org = self.createModelInstance(Organization, name="testorg")        # CREATE THE ORGANIZATION
        self.membership = self.createModelInstance(Membership, user=self.user, org=self.org)        # ADD THE MEMBERSHIP

    def test_create_protocol(self):
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")
        self.assertEquals(self.protocol.raw, "what?")
        self.assertEquals(self.protocol.slug, "%d-test-protocol" % self.protocol.pk)

    def test_protocol_keygen(self):
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")
        key1 = self.protocol.get_hash_id()
        key2 = self.protocol.get_hash_id()
        self.assertNotEqual(key1, key2)             # CONFIRM THAT THE KEYGEN IS UNIQUE EACH TIME

    def test_step_add(self):
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")
        step1 = Step(self.protocol, data={"name":"step1"})

        self.assertEquals(len(self.protocol.steps), 1)   # STEP SHOULD REGEISTER IT'S SELF WITH THE PROTOCOL
        self.assertTrue('objectid' in step1)        # STEP SHOULD GET OBJECT ID AFTER REGISTERED
        self.assertEquals(step1['slug'], step1['objectid'])

        step2 = Step(self.protocol, data={"name":"step2"})
        self.assertEquals(len(self.protocol.steps), 2)   # STEP SHOULD REGEISTER IT'S SELF WITH THE PROTOCOL
        self.assertTrue('objectid' in step2)        # STEP SHOULD GET OBJECT ID AFTER REGISTERED
        self.assertEquals(step2['slug'], step2['objectid'])

    # def test_action_add(self):
    #     self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?")

    #     step1 = Step(self.protocol, name="step1")
    #     # print "STEP 1 ID: %s" % step1['objectid']

    #     # NEED TO MAKE TEST ACTION WITH EXPECTED FAILURE FOR NOT GETTING VERB ARGUMENT PASSED
    #     # self.assertRaises(KeyError, Action, (protocol, parent=step1))

    #     a1 = Action(self.protocol, parent=step1, data={'verb':"add"})
    #     # print "ACTION 1 ID: %s" % a1['objectid']

    # #     # print "PROTOCOL DATA:"
    # #     # print protocol.data

    # #     # print "PROTOCOL NODES:"
    # #     # print protocol.nodes

    #     self.assertEquals(len(step1.actions), 1)    # ASSERT THE ACTION IS ATTACHED TO THE STEP
    # #     self.assertTrue('objectid' in a1)           # ACTION SHOULD GET OBJECT ID AFTER REGISTERED
    # #     self.assertEquals(len(self.protocol.nodes), 2)   # ASSERT THAT THE ACTION WAS ADDED TO THE PROTOCOL AS WELL
    # #     self.assertEquals(a1['slug'], a1['objectid'])


