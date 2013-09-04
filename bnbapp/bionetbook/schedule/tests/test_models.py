from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component

from organization.models import Organization, Membership
from workflow.models import Workflow
from experiment.models import Experiment
from schedule.models import Calendar
from api.tests.core import AutoBaseTest
from django.utils import simplejson as json


class CalendarModelTests(AutoBaseTest):

	def setUp(self):
		super(CalendarModelTests, self).setUp()

		self.user = self.createUserInstance(username="testuser", password="pass", email="test@example.com")
		self.profile = self.createModelInstance(Profile, user=self.user)
		self.org = self.createModelInstance(Organization, name="TestOrg")
		self.member = self.createModelInstance(Membership, user=self.user, org=self.org)
		self.workflow = self.createModelInstance(Workflow, user=self.user, name="TestWorkflow", data={'meta':{},'protocols':[1]})
		self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, data=
		{
			"steps": [ {
					"objectid":"8v5lak",
      				"name": "1", 
      				"actions": [ {
          				"name": "first action", 
          				"objectid": "kxsl3b", 
          				"verb": "add", 
          				"duration": "0-0", 
          				"slug": "kxsl3b"
          				},
						{
          				"name": "second action", 
          				"objectid": "xxxxxx", 
          				"verb": "mix", 
          				"duration": "0-0", 
          				"slug": "xxxxxx"
          				} ]
				} ] 
		} )
		self.experiment = self.createModelInstance(Experiment, user=self.user, workflow=self.workflow, name="Test Experiment")
		self.calendar = self.createModelInstance(Calendar, user=self.user, name="Test Schedule")

	def test_calendar_setup(self):
		caldata = {
			'meta':{},
			'events': [ {
							'id':"bnb-o1-e1-p1-8v5lak-kxsl3b",
                            'start':'0',
                            'duration':'0',
                            'title':"first action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment',
                            'notes':"",
                            'verb':"add"
						},
						{
							'id':"bnb-o1-e1-p1-8v5lak-xxxxxx",
                            'start':'0',
                            'duration':'0',
                            'title':"second action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment',
                            'notes':"",
                            'verb':"mix"						
						} ]
					}
		self.assertEqual(self.calendar.data,caldata)

	def test_calendar_update(self):
		self.experiment2 = self.createModelInstance(Experiment, user=self.user, workflow=self.workflow, name="Test Experiment 2")
		self.calendar.addExperiment(self.experiment2)
		caldata = {
			'meta':{},
			'events': [ {
							'id':"bnb-o1-e1-p1-8v5lak-kxsl3b",
                            'start':'0',
                            'duration':'0',
                            'title':"first action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment',
                            'notes':"",
                            'verb':"add"
						},
						{
							'id':"bnb-o1-e1-p1-8v5lak-xxxxxx",
                            'start':'0',
                            'duration':'0',
                            'title':"second action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment',
                            'notes':"",
                            'verb':"mix"						
						},
{
							'id':"bnb-o1-e2-p1-8v5lak-kxsl3b",
                            'start':'0',
                            'duration':'0',
                            'title':"first action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment 2',
                            'notes':"",
                            'verb':"add"
						},
						{
							'id':"bnb-o1-e2-p1-8v5lak-xxxxxx",
                            'start':'0',
                            'duration':'0',
                            'title':"second action",
                            'protocol':'Test Protocol',
                            'experiment':'Test Experiment 2',
                            'notes':"",
                            'verb':"mix"						
						} ]
					}
		self.assertEqual(self.calendar.data,caldata)
