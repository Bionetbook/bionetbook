from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
from workflow.models import Workflow
from experiment.models import Experiment
from schedule.models import Calendar

from organization.models import Organization, Membership
from schedule.tests.core import AutoBaseTest

class ScheduleViewTests(AutoBaseTest):

	def setUp(self):
		super(ScheduleViewTests, self).setUp()

	def test_create_calendar(self):
		print "testing"

