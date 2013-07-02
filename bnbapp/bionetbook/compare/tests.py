"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.db import models
from django.test import TestCase
from protocols.utils import MANUAL_VERBS, MACHINE_VERBS, COMPONENT_VERBS, THERMOCYCLER_VERBS, MANUAL_LAYER, settify, labeler 
from protocols.models import Protocol, Action, Step


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ManualVerbTest(TestCase):
	def test_verb_is_manual(self):
		from CompareVerb import get_manual_node
		'tests that the verb is a manual verb'
		expected = 'manual'
		protocol = Protocol.objects.get(pk=19)
		


		actual = self.
		self.assertEqual()