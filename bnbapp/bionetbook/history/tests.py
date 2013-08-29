"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
1. catch change in protocol keys
2. catch added step 
3. catch removed step 
4. catch edited step 
5. catch edited step children 
6. catch added action 
7. catch removed action 
8. catch edited action 
9. catch edited step action 
10. catch added child 
11. catch removed child
12. catch edited child 
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_added_step(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)



