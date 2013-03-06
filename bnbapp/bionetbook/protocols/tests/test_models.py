from django.contrib.auth.models import User
from django.test import TestCase

# from actions.models import Action
from protocols.models import Protocol, Action, Step, Component
# from steps.models import Step
from organization.models import Organization, Membership

class ProtocolModelTests(TestCase):

    def setUp(self):

        # CREATE THE USER
        self.user = User.objects.create_user( username="testuser", password="password", email="test@example.com" )
        self.user.save()

        # CREATE THE ORGANIZATION
        self.org = Organization.objects.create(name="testorg")
        self.org.save()

        # ADD THE MEMBERSHIP
        m = Membership(user=self.user, org=self.org)
        m.save()

    def test_create_protocol(self):
        protocol = Protocol.objects.create( name="Test Protocol", owner=self.org, raw="what?" )
        self.assertEquals(protocol.raw, "what?")
        self.assertEquals(protocol.slug, "test-protocol")

    def test_protocol_keygen(self):
        protocol = Protocol.objects.create( name="Test Protocol", owner=self.org, raw="what?" )
        key1 = protocol.get_hash_id()
        key2 = protocol.get_hash_id()
        self.assertNotEqual(key1, key2)             # CONFIRM THAT THE KEYGEN IS UNIQUE EACH TIME

    def test_step_add(self):
        protocol = Protocol.objects.create( name="Test Protocol", owner=self.org, raw="what?" )
        step1 = Step(protocol, data={"name":"step1"})

        self.assertEquals(len(protocol.steps), 1)   # STEP SHOULD REGEISTER IT'S SELF WITH THE PROTOCOL
        self.assertTrue('objectid' in step1)        # STEP SHOULD GET OBJECT ID AFTER REGISTERED
        self.assertEquals(step1['slug'], step1['objectid'])

        step2 = Step(protocol, data={"name":"step2"})
        self.assertEquals(len(protocol.steps), 2)   # STEP SHOULD REGEISTER IT'S SELF WITH THE PROTOCOL
        self.assertTrue('objectid' in step2)        # STEP SHOULD GET OBJECT ID AFTER REGISTERED
        self.assertEquals(step2['slug'], step2['objectid'])

    def test_actions(self):
        protocol = Protocol.objects.create( name="Test Protocol", owner=self.org, raw="what?" )

        step1 = Step(protocol, name="step1")
        # print "STEP 1 ID: %s" % step1['objectid']

        # NEED TO MAKE TEST ACTION WITH EXPECTED FAILURE FOR NOT GETTING VERB ARGUMENT PASSED
        # self.assertRaises(KeyError, Action, (protocol, parent=step1))

        a1 = Action(protocol, parent=step1, data={'verb':"add"})
        # print "ACTION 1 ID: %s" % a1['objectid']

        # print "PROTOCOL DATA:"
        # print protocol.data

        # print "PROTOCOL NODES:"
        # print protocol.nodes

        self.assertEquals(len(step1.actions), 1)    # ASSERT THE ACTION IS ATTACHED TO THE PROTOCOL
        self.assertTrue('objectid' in a1)           # ACTION SHOULD GET OBJECT ID AFTER REGISTERED
        self.assertEquals(len(protocol.nodes), 2)   # ASSERT THAT THE ACTION WAS ADDED TO THE PROTOCOL AS WELL
        self.assertEquals(a1['slug'], a1['objectid'])
