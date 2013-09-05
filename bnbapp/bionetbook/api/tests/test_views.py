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
		self.user2 = self.createUserInstance(username="fakeuser", password="pass", email="fake@example.com")
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
          				"name": "first action", 
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

		# Testing successful GET
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.get('/api/calendar/1/')
		self.assertEqual(resp.status_code, 200)
		cal = 	{
					'meta':{},
					'events':[ {
							 	'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
							 	'start':'0',
							 	'duration':'0',
							 	'title':'first action',
							 	'protocol':'Test Protocol',
							 	'experiment':'Test Experiment',
							 	'notes':'',
							 	'verb':'add'
								} ]
				}
		self.assertEqual(json.loads(resp.content),cal)

		# Testing failed GET, should return 404
		resp2 = c.get('/api/calendar/2/')
		self.assertEqual(resp2.status_code, 404)

	def test_list_calendar_api(self):

		# Testing successful GET
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.get('/api/calendar/')
		ret = { 'calendars': ['Test Schedule-1']}
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(json.loads(resp.content), ret)

	def test_single_event_api(self):

		# Testing successful GET
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.get('/api/calendar/1/bnb-o1-e1-p1-8v5lak-kxsl3b/')
		self.assertEqual(resp.status_code, 200)
		event = {
					'protocol':'Test Protocol',
					'duration':'0',
					'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
					'title':'first action',
					'verb':'add',
					'notes':'',
					'experiment':'Test Experiment',
					'start':'0'
				}
		self.assertEqual(json.loads(resp.content), event)
		
		# Testing with wrong id, should return 404
		resp2 = c.get('/api/calendar/1/bnb-o1-e1-p1-8v5lak-kxsl3x/')
		self.assertEqual(resp2.status_code, 404)
		
		# Testing with wrong calendar pk
		resp3 = c.get('/api/calendar/2/bnb-o1-e1-p1-8v5lak-kxsl3b/')
		self.assertEqual(resp3.status_code, 404)

		# Testing successful PUT
		update = {
						'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
						'start':'5',
						'notes':'new notes'
				 }
		resp4 = c.put('/api/calendar/1/bnb-o1-e1-p1-8v5lak-kxsl3b/', data=update)
		self.assertEqual(resp4.status_code, 200)
		ret = {
					'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
					'start':'5',
					'notes':'new notes',
					'status':'updated'
				}
		self.assertEqual(json.loads(resp4.content), ret)

		# Testing successful GET after updating event
		resp5 = c.get('/api/calendar/1/bnb-o1-e1-p1-8v5lak-kxsl3b/')
		eventUpdated = {
					'protocol':'Test Protocol',
					'duration':'0',
					'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
					'title':'first action',
					'verb':'add',
					'notes':'new notes',
					'experiment':'Test Experiment',
					'start':'5'
				}
		self.assertEqual(json.loads(resp5.content), eventUpdated)
		self.assertEqual(resp5.status_code, 200)

		# Testing failed PUT, should return 404 for both incorrect calendar pk and event id
		update2 = {
						'id':'bnb-o1-e1-p1-8v5lak-kxsl3x',
						'start':'5',
						'notes':'new notes'
				 }
		resp6 = c.put('/api/calendar/1/bnb-o1-e1-p1-8v5lak-kxsl3x/', data=update2)
		self.assertEqual(resp6.status_code, 404)
		resp6 = c.put('/api/calendar/2/bnb-o1-e1-p1-8v5lak-kxsl3x/', data=update2)
		self.assertEqual(resp6.status_code, 404)

