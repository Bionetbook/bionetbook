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
<<<<<<< HEAD
from schedule.models import Calendar


class ScheduleViewTests(TestCase):
	def CalendarModelTest(self):
		cal = Calendar()
		cal.data = {'steps':[{'actions':[{'name':'mix','verb':'mix'}]},{'actions':[{'name':'add','verb':'add'}]}]}
		output = cal.dataToCalendar()
		print output
