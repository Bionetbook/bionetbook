from django.contrib.auth.models import User
from django.test import TestCase

# from actions.models import Action
from protocols.models import Protocol, Action, Step, Component
# from steps.models import Step
from organization.models import Organization

class ProtocolModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )
        self.user.save()
        self.organization = Organization.objects.create(name="testorg")
        #self.user.organization.append(self.organization)
        #print dir(self.organization.members)
        #print self.organization.members
        #self.organization.members.add(self.user)
        #print dir(self.user)

    def test_create_protocol(self):

        protocol = Protocol.objects.create(
            name="Test Protocol",
            owner=self.organization,
            raw="what?"
            )
        self.assertEquals(protocol.raw, "what?")

    def test_actions(self):
        protocol = Protocol.objects.create(
            name="Test Protocol",
            owner=self.organization,
            raw="what?"
            )
        step1 = Step(protocol=protocol, parent=protocol)
        a1 = Action(protocol=protocol, parent=step1, verb="add")
        # Action.objects.create(step=step1)
        # Action.objects.create(step=step1)
        # Action.objects.create(step=step1)
        # step2 = Step.objects.create(protocol=protocol)
        # Action.objects.create(step=step2)
        # Action.objects.create(step=step2)
        # Action.objects.create(step=step2)
        # self.assertEquals(len(protocol.nodes), 2) # NEED TO TEST THIS OUT AND SEE WHY IT BREAKS
