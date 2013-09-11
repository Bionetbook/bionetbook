from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component

from organization.models import Organization, Membership
from workflow.models import Workflow
from experiment.models import Experiment
from schedule.models import Calendar
from organization.tests.core import AutoBaseTest
from django.utils import simplejson as json

class OrganizationViewTests(AutoBaseTest):

	def setUp(self):
		super(OrganizationViewTests, self).setUp()

		self.user = self.createUserInstance(username="testuser1", password="pass", email="test1@example.com")
		self.user2 = self.createUserInstance(username="testuser2", password="pass", email="test2@example.com")
		self.user3 = self.createUserInstance(username="testuser3", password="pass", email="test3@example.com")
		self.profile = self.createModelInstance(Profile, user=self.user)
		self.profile2 = self.createModelInstance(Profile, user=self.user2)
		self.profile3 = self.createModelInstance(Profile, user=self.user3)
		self.org = self.createModelInstance(Organization, name="TestOrg", slug="testorg")
		self.org2 = self.createModelInstance(Organization, name="Test2Org", slug="test2org")
		self.member = self.createModelInstance(Membership, user=self.user, org=self.org)
		self.member2 = self.createModelInstance(Membership, user=self.user2, org=self.org)
		self.member3 = self.createModelInstance(Membership, user=self.user3, org=self.org2)
		self.protocol = self.createModelInstance(Protocol, name="Test1", owner=self.org, author=self.user)
		self.protocol2 = self.createModelInstance(Protocol, name="Test2", owner=self.org, author=self.user2)
		self.protocol3 = self.createModelInstance(Protocol, name="Test3", owner=self.org, author=self.user2, published=True)
		self.protocol4 = self.createModelInstance(Protocol, name="Test4", owner=self.org2, author=self.user3)
		self.workflow = self.createModelInstance(Workflow, user=self.user, name="TestFlow", data={'meta':{},'protocols':[1]}, owner=self.org)
		self.workflow2 = self.createModelInstance(Workflow, user=self.user2, name="TestFlow2", data={'meta':{},'protocols':[3,2]}, owner=self.org)
		self.workflow3 = self.createModelInstance(Workflow, user=self.user3, name="TestFlow3", data={'meta':{},'protocols':[4]}, owner=self.org2)
		self.experiment = self.createModelInstance(Experiment, owner=self.org, user=self.user, name="Exp1", workflow=self.workflow)
		self.experiment2 = self.createModelInstance(Experiment, owner=self.org, user=self.user2, name="Exp2", workflow=self.workflow2)
		self.experiment3 = self.createModelInstance(Experiment, owner=self.org2, user=self.user3, name="Exp3", workflow=self.workflow3)

	def test_experiment_detail(self):
		# testing context for detail view
		c = Client()
		c.login(username="testuser1", password="pass")
		resp = c.get('/testorg/experiments/1-exp1/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['experiment'],self.experiment)
		self.assertEqual(resp.context['workflow'], self.workflow)
		self.assertEqual(resp.context['organization'],self.org)
		resp = c.get('/test2org/experiments/1-exp1/')
		self.assertEqual(resp.status_code, 404)
		resp = c.get('/testorg/experiments/2-exp2/')
		self.assertEqual(resp.status_code, 404)

	def test_experiment_create(self):
		c = Client()
		c.login(username="testuser1", password="pass")
		resp = c.get('/testorg/experiments/create/')
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context['form'].fields['workflows'].choices, [(1,self.workflow)])
		resp = c.get('/test2org/experiments/create/')
		self.assertEqual(resp.status_code, 404)