from django.contrib.auth.models import User
from django.test import TestCase

from actions.models import Action
from protocols.models import Protocol
from steps.models import Step


class ProtocolModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            email="test@example.com"
            )

    def test_create_protocol(self):

        protocol = Protocol.objects.create(
            name="Test Protocol",
            owner=self.user,
            raw="what?"
            )
        self.assertEquals(protocol.raw, "what?")

    def test_actions(self):
        protocol = Protocol.objects.create(
            name="Test Protocol",
            owner=self.user,
            raw="what?"
            )
        step1 = Step.objects.create(protocol=protocol)
        Action.objects.create(step=step1)
        Action.objects.create(step=step1)
        Action.objects.create(step=step1)
        step2 = Step.objects.create(protocol=protocol)
        Action.objects.create(step=step2)
        Action.objects.create(step=step2)
        Action.objects.create(step=step2)
        self.assertEquals(protocol.actions.count(), 6)
