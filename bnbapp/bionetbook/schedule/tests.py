"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
from organization.models import Organization, Membership


class ScheduleViewTests(TestCase):
	def test_default(self):
		self.assertEqual(1,1)
