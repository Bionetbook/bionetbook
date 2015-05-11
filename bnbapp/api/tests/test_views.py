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
          				"physical_commitment":"Passive" 
        			}
      			], 
      			"duration": "0-0", 
      			"slug": "8v5lak", 
    		} ]
		})
		self.protocol2 = self.createModelInstance(Protocol, name="Test Protocol 2", owner=self.org, data=
  		{
  			"steps": [ {
      				"objectid": "xxxxxx", 
      				"name": "1", 
      				"actions": [ {
          				"name": "first action", 
          				"objectid": "yyyyyy", 
          				"verb": "add", 
          				"duration": "0-0", 
          				"slug": "yyyyyy", 
          				"physical_commitment":"Passive"
        			}
      			], 
      			"duration": "0-0", 
      			"slug": "xxxxxx", 
    		} ]
		})
		self.workflow = self.createModelInstance(Workflow, owner=self.org, user=self.user, name="TestWorkflow", data={'meta':{},'protocols':[1,2]})
		self.experiment = self.createModelInstance(Experiment, owner=self.org, user=self.user, workflow=self.workflow, name="Test Experiment")
		self.calendar = self.createModelInstance(Calendar, user=self.user, name="Test Schedule")

	def test_protocol_list_api(self):
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.post('/api/testorg/protocolList/', data={'name':'workflow2','protocols':[{'name':'test2','pk':2},{'name':'test1','pk':1}]})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp['location'],'http://testserver/testorg/workflows/2-workflow2/')
		resp = c.get('/testorg/workflows/2-workflow2/')
		self.assertEqual(resp.context['protocols'],[self.protocol2,self.protocol])

	def test_single_calendar_api(self):

		# Testing successful GET
		c = Client()
		c.login(username="testuser", password="pass")
		resp = c.get('/api/calendar/1/')
		self.assertEqual(resp.status_code, 200)
		cal = 	{
					'meta':{ '1': None, '2': None},
					'events':[ {
							 	'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
							 	'start':'0',
							 	'duration':'0',
							 	'title':'first action',
							 	'protocol':'Test Protocol',
							 	'experiment':'Test Experiment',
							 	'notes':'',
							 	'verb':'add',
							 	'active':'false'
								}, 
								{
								'id':'bnb-o1-e1-p2-xxxxxx-yyyyyy',
								'start':'0',
								'duration':'0',
								'title':'first action',
								'protocol':'Test Protocol 2',
								'experiment': 'Test Experiment',
								'notes':'',
								'verb':'add',
								'active':'false'
								} ]
				}
		self.assertEqual(json.loads(resp.content),cal)

		# Testing failed GET, should return 404
		resp2 = c.get('/api/calendar/2/')
		self.assertEqual(resp2.status_code, 404)

		# Testing PUT
		p = {
						'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
						'start':'5',
						'notes':'new notes'
				 }
		p2 = {
						'id':'bnb-o1-e1-p2-xxxxxx-yyyyyy',
						'start':'10',
						'notes':'new notes'
				 }
		events = {'events':[p, p2]}
		resp3 = c.put('/api/calendar/1/', data=events)
		self.assertEqual(resp3.status_code, 200)

		resp4 = c.get('/api/calendar/1/')
		self.assertEqual(resp4.status_code, 200)
		cal = 	{
					'meta':{ '1': None, '2': None},
					'events':[ {
							 	'id':'bnb-o1-e1-p1-8v5lak-kxsl3b',
							 	'start':'5',
							 	'duration':'0',
							 	'title':'first action',
							 	'protocol':'Test Protocol',
							 	'experiment':'Test Experiment',
							 	'notes':'new notes',
							 	'verb':'add',
							 	'active':'false'
								},
								{
								'id':'bnb-o1-e1-p2-xxxxxx-yyyyyy',
								'start':'10',
								'duration':'0',
								'title':'first action',
								'protocol':'Test Protocol 2',
								'experiment': 'Test Experiment',
								'notes':'new notes',
								'verb':'add',
								'active':'false'
								} ]
				}
		self.assertEqual(json.loads(resp4.content),cal)

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
					'start':'0',
					'active':'false'
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
					'start':'5',
					'active':'false'
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

