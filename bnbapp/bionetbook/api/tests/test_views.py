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

class APIViewTests(AutoBaseTest):

	def setUp(self):
		super(APIViewTests, self).setUp()

		self.user = self.createUserInstance(username="testuser", password="pass", email="test@example.com")
		self.profile = self.createModelInstance(Profile, user=self.user)
		self.org = self.createModelInstance(Organization, name="TestOrg")
		self.member = self.createModelInstance(Membership, user=self.user, org=self.org)
		self.workflow = self.createModelInstance(Workflow, user=self.user, name="TestWorkflow", data={'meta':{},'protocols':[1]})
		self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, data=
  		{
  			"steps": [ {
      				"objectid": "8v5lak", 
      				"name": "1", 
      				"actions": [ {
          				"name": "add", 
          				"objectid": "kxsl3b", 
          				"verb": "add", 
          				"duration": "0-0", 
          				"slug": "kxsl3b", 
        			}
      			], 
      			"duration": "0-0", 
      			"slug": "8v5lak", 
    		} ]
		})
		self.experiment = self.createModelInstance(Experiment, user=self.user, workflow=self.workflow, name="Test Experiment")
		self.calendar = self.createModelInstance(Calendar, user=self.user, name="Test Schedule")


	def test_single_calendar_api(self):
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.get('/api/calendar/1/')
		self.assertEqual(resp.status_code, 200)
		cal = {'meta':{},'events':[{'id':'bnb-o1-e1-p1-8v5lak-kxsl3b','start':'0','duration':'0','action':'add', 'protocol':'Test Protocol', 'experiment':'Test Experiment','notes':''}]}
		rep = json.loads(resp.content)
		self.assertEqual(rep,cal)
