"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

class AutoBaseTest(TestCase):

    def createUserInstance(self, **kwargs):
        '''Method to create a user and register it with the teardown operation'''
        m = User.objects.create_user( **kwargs )
        self.teardownList.append(m)
        return m

    def createModelInstance(self, model, **kwargs):
        '''Method to create any Model instance and register it with the teardown operation'''
        m = model( **kwargs )
        m.save()
        self.teardownList.append(m)
        return m

    def setUp(self):
        self.teardownList = []

    def tearDown(self):
        self.teardownList.reverse()     # Reverse the list's creation order

        for item in self.teardownList:
            item.delete()
