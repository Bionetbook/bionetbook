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

import pprint
pp = pprint.PrettyPrinter(indent=4)
import sys

from django.test import TestCase
from core.tests import AutoBaseTest

from protocols.models import Protocol, Action, Step, Component, Thermocycle, Machine
from organization.models import Organization, Membership
from history.models import History

# class SimpleTest(TestCase):
#     def test_added_step(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)



class HistoryModelTests(AutoBaseTest):

    def setUp(self):
        super(HistoryModelTests, self).setUp()
        self.protocol = None
        self.user = self.createUserInstance( username="testuser", password="password", email="test@example.com" )        # CREATE THE USER
        self.org = self.createModelInstance(Organization, name="testorg")        # CREATE THE ORGANIZATION
        self.membership = self.createModelInstance(Membership, user=self.user, org=self.org)        # ADD THE MEMBERSHIP
        self.protocol = self.createModelInstance(Protocol, name="Test Protocol", owner=self.org, raw="what?", author=self.user)

    def test_history_logging_for_protocol(self):
        
        history = self.protocol.history_set.all()

        self.assertEquals(len(history), 1)
        self.assertEquals(history[0].data['create'][0]['id'], 1)
        self.assertEquals(history[0].data['create'][0]['attrs']['name'], "Test Protocol")
        
    
    def test_catch_change_in_protocol_values(self):
        
        self.protocol.name = "New Test Protocol"
        self.protocol.save()

        history = self.protocol.history_set.all()

        self.assertEquals(len(history), 2)
        self.assertEquals(history[0].data['update'][0]['id'], 1)
        self.assertEquals(history[0].data['update'][0]['attrs']['name'], "New Test Protocol")
        

    def test_catch_change_in_published_protocol_values(self):

        self.protocol.name = "New Published Protocol"
        self.protocol.published = True
        self.protocol.save()

        history = self.protocol.history_set.all()

        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history), 2)
        self.assertEquals(history[0].data['update'][0]['id'], 1)
        self.assertEquals(history[0].data['update'][0]['attrs']['name'], "New Published Protocol")
        self.assertEquals(history[0].data['update'][0]['attrs']['published'], True)

    def test_change_two_attrs_in_published_protocol_values(self):

        self.protocol.name = "First Name Protocol"
        self.protocol.save()

        self.protocol.name = "New Published Protocol"
        self.protocol.published = True
        self.protocol.save()

        history = self.protocol.history_set.all()

        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history), 3)
        self.assertEquals(history[0].data['update'][0]['attrs']['name'], "New Published Protocol")

    def test_log_adding_step_to_protocol(self):
        
        self.protocol.published = True
        step = Step(self.protocol)
        self.protocol.add_node(step)
        self.protocol.save()            # <- Not Currently being logged

        # print "\nSTEP ADDED:"
        # pp.pprint( step )

        # print "\nPROTOCOL STEP DATA:"
        # pp.pprint( self.protocol.data )

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        # print history[0].data['create'][0]['attrs']
        self.assertEquals(len(history[0].data['update']), 1)                    # LOG THE PUBLISH CHANGE
        self.assertEquals(history[0].data['create'][0]['type'], 'step')    # STEP SHOULD SHOW UP AS A CREATION

    def test_log_adding_two_protocols(self):
        
        self.protocol.published = True
        protocol_two = self.createModelInstance(Protocol, name="Second Protocol", owner=self.org, raw="", author=self.user)

        self.protocol.published = True
        self.protocol.save()

        history = History.objects.all()
        history_one = self.protocol.history_set.all()

        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history_one), 2)
        self.assertEquals(len(history), 3)

        # print history[0].data['create'][0]['attrs']
        # self.assertEquals(len(history[0].data['update']), 1)                    # LOG THE PUBLISH CHANGE
        # self.assertEquals(history[0].data['create'][0]['type'], 'step')    # STEP SHOULD SHOW UP AS A CREATION



    def test_log_adding_multiple_nodes_to_protocol(self):
        
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                      # UPDATE TO THE STEP IN THE PROTOCOL

        action = Action(self.protocol, parent=step, verb="add")     # ACTION NOT BEING ADDED CORRECTLY HERE
        step.add_child_node(action)                                     # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history[1].data['update']), 1)                    # LOG THE PUBLISH CHANGE
        self.assertEquals(history[1].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

        # ADD TESTS FOR ACTION ADD LOG
        self.assertEquals(history[0].data['create'][0]['type'], 'action')   # ACTION SHOULD SHOW UP AS A CREATION

    def test_log_adding_multiple_component_nodes_to_protocol(self):
        
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="add")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        comp1 = Component(self.protocol, parent=action1)
        comp2 = Component(self.protocol, parent=action1)
        self.protocol.save()

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history[2].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[2].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

        # ADD TESTS FOR ACTION ADD LOG
        self.assertEquals(history[0].data['create'][0]['type'], 'component')
        self.assertEquals(history[0].data['create'][1]['type'], 'component')    
            # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.assertEquals(len(history[0].data['update']), 2)
        self.assertIn('duration', history[0].data['update'][0]['attrs'])
        self.assertIn('duration', history[0].data['update'][1]['attrs'])


    # def test_log_adding_multiple_thermocycle_nodes_to_action(self):
    #     # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
    #     self.protocol.published = True
    #     step = Step(self.protocol, data={"name":"step1"})
    #     self.protocol.save() # his[2]
    #     step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

    #     action1 = Action(self.protocol, parent=step, verb="thermocycle")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
    #     step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
    #     self.protocol.save() # his[1]

    #     phase1 = Thermocycle(self.protocol, parent=action1, data = {"name": "first", "min_time": 0, "cycles": "","cycle_back_to":""})
    #     phase2 = Thermocycle(self.protocol, parent=action1, data = {"name": "second", "min_time": 0, "cycles": "","cycle_back_to":""})
        
    #     self.protocol.save() # his[0]

    #     history = self.protocol.history_set.all()
    #     for h in history:
    #         print "\nHISTORY EVENT: %d" % h.pk
    #         pp.pprint( h.data )

    #     self.assertEquals(len(history[2].data['update']), 1)                # LOG THE PUBLISH CHANGE
    #     self.assertEquals(history[2].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

    #     # ADD TESTS FOR ACTION ADD LOG
    #     self.assertEquals(history[0].data['create'][0]['type'], 'thermocycle')
    #     self.assertEquals(history[0].data['create'][1]['type'], 'thermocycle')    
        
    #         # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
    #     self.assertEquals(len(history[0].data['update']), 2)
    #     self.assertIn('duration', history[0].data['update'][0]['attrs'])
    #     self.assertIn('duration', history[0].data['update'][1]['attrs'])

    def test_log_adding_machine_node_to_action(self):
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="centrifuge")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        machine1 = Machine(self.protocol, parent=action1, data={'name':'microcentrifuge', "min_time": 1, "time_units": 'sec'})
        # comp2 = Component(self.protocol, parent=action1)
        self.protocol.save()

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history[2].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[2].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

        # ADD TESTS FOR ACTION ADD LOG
        self.assertEquals(history[0].data['create'][0]['type'], 'machine')
        
            # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.assertEquals(len(history[0].data['update']), 2)
        self.assertIn('duration', history[0].data['update'][0]['attrs'])
        self.assertIn('duration', history[0].data['update'][1]['attrs'])

    def test_log_editing_multiple_component_nodes_to_action(self):    
        # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="add")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        comp1 = Component(self.protocol, parent=action1)
        comp2 = Component(self.protocol, parent=action1)
        # comp2 = Component(self.protocol, parent=action1)
        self.protocol.save()
        # comp1['name']='NaCl'
        comp1["min_conc"]= 5
        comp1["conc_units"]= "mM"
        comp2["max_conc"]= 10
        comp2["name"]= "bleach"
        self.protocol.save()

        history = self.protocol.history_set.all()
        for h in history:
            print "\nHISTORY EVENT: %d" % h.pk
            pp.pprint( h.data )

        self.assertEquals(len(history[3].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[3].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

        # TEST THAT COMPONENT ATTRS WERE UPDATED
        self.assertEquals(len(history[0].data['update'][0]['attrs']), 2)
        self.assertEquals(len(history[0].data['update'][1]['attrs']), 2)

    def test_log_editing_multiple_thermocycle_nodes_to_action(self):    
        # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        pass    

    def test_log_editing_machine_node_to_action(self):    
        # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="centrifuge")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        machine1 = Machine(self.protocol, parent=action1, data={'name':'microcentrifuge', "min_time": 1, "time_units": 'sec'})
        # comp2 = Component(self.protocol, parent=action1)
        self.protocol.save()
        machine1['name']='speedvac'
        machine1["min_time"]= 5
        self.protocol.save()

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        self.assertEquals(len(history[3].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[3].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION

        # TEST THAT MACHINE WAS UPDATED
            # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.assertEquals(len(history[0].data['update']), 3)
        updated_types = []
        
        # TEST IF NAME AND DURATION WERE CHANGED
        for cnt, item in enumerate(history[0].data['update']):
            updated_types.append(item['type'])
            if item['type'] =='machine':
                updated = item
            # TEST IF ACTION AND STEP WERE UPDATED    
            if item['type'] =='action' or item['type'] =='step':
                self.assertIn('duration', item['attrs'])    


        self.assertIn('machine', updated_types)                      
        self.assertIn('name', updated['attrs']) 
        self.assertIn('min_time', updated['attrs']) 

    def test_log_adding_and_removing_step_from_protocol(self):
        self.protocol.published = True
        step = Step(self.protocol)
        # print "ADDED STEP ID: %s" %step['objectid']
        self.protocol.add_node(step)
        self.protocol.save()    # <- Not Currently being logged

        history = self.protocol.history_set.all()
        
        self.assertEquals(len(history[0].data['update']), 1)                    # LOG THE PUBLISH CHANGE
        self.assertEquals(history[0].data['create'][0]['type'], 'step')

        self.protocol.delete_node(step['objectid'])
        self.protocol.save()

        # print "\nSTEP ADDED:"
        # pp.pprint( step )

        # print "\nPROTOCOL STEP DATA:"
        # pp.pprint( self.protocol.data )
        history = self.protocol.history_set.all()

        self.assertEquals(len(history[0].data['delete']), 1)                    # LOG THE PUBLISH CHANGE
        self.assertEquals(history[0].data['delete'][0]['type'], 'step')
        
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

    def test_log_adding_and_removing_action_from_step(self):
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                      # UPDATE TO THE STEP IN THE PROTOCOL

        action = Action(self.protocol, parent=step, verb="add")     # ACTION NOT BEING ADDED CORRECTLY HERE
        step.add_child_node(action)                                     # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        self.protocol.delete_node(action['objectid'])
        self.protocol.save()
    
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        history = self.protocol.history_set.all()
        
        self.assertEquals(len(history[0].data['delete']), 1)                    # LOG THE PUBLISH CHANGE
        self.assertEquals(history[0].data['delete'][0]['type'], 'action')

    def test_log_adding_two_actions_and_removing_one_action_from_step(self):
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                      # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="add")
        action2 = Action(self.protocol, parent=step, verb="mix")     # ACTION NOT BEING ADDED CORRECTLY HERE
        self.protocol.save()

        self.protocol.delete_node(action1['objectid'])
        self.protocol.save()

        history = self.protocol.history_set.all()

        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )
        
        self.assertEquals(len(history), 4)
        self.assertEquals(len(history[0].data['delete']), 1)                    # LOG THE DELETE CHANGE
        self.assertEquals(history[0].data['delete'][0]['type'], 'action')
        
    def test_log_adding_and_deleting_a_component_to_actions(self):    
        
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save() #2 / 3
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="add")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save() #3 / 2

        comp1 = Component(self.protocol, parent=action1, name='comp1')
        comp2 = Component(self.protocol, parent=action1, name='comp2')
        self.protocol.save() #4 / 1

        self.protocol.delete_node(comp1['objectid'])
        self.protocol.save() #5 / 0

        history = self.protocol.history_set.all()
        # for h in history:
        #     print "\nHISTORY EVENT: %d" % h.pk
        #     pp.pprint( h.data )

        # TEST THAT OBJECT IS CONSTRUCTED PROPERLY

        self.assertEquals(len(history[3].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[3].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION
        self.assertEquals(history[2].data['create'][0]['type'], 'action')
        
        # TESTS FOR ADDING 2 COMPONENTS TO ACTION
        self.assertEquals(history[1].data['create'][0]['type'], 'component')
        self.assertEquals(history[1].data['create'][1]['type'], 'component')
        
        # TEST THAT COMPONENT IS BEING DELETED
        self.assertEquals(len(history[0].data['delete']), 1)
        self.assertEquals(history[0].data['delete'][0]['type'], 'component')

            # TEST THAT DURATION IS GETTING UPDATED
        self.assertEquals(len(history[0].data['update']), 2)                
        self.assertIn('duration', history[0].data['update'][0]['attrs'])
        self.assertIn('duration', history[0].data['update'][1]['attrs'])
        
        
    def test_log_deleting_multiple_thermocycle_nodes_from_action(self):
        # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        pass

    def test_log_deleting_machine_node_from_action(self):
        # TESTS THAT ACTION AND STEP DURATION ARE UPDATED
        self.protocol.published = True
        step = Step(self.protocol, data={"name":"step1"})
        self.protocol.save()
        step = self.protocol.data['steps'][-1]                              # UPDATE TO THE STEP IN THE PROTOCOL

        action1 = Action(self.protocol, parent=step, verb="centrifuge")            # ACTION IS NOT ASSIGNING IT'S SELF TO THE PARENT, THIS NEEDS A DEEP FIX
        step.add_child_node(action1)                                        # <- WORKS ONLY AFTER STEP IS RE-ASSIGNED
        self.protocol.save()

        machine1 = Machine(self.protocol, parent=action1, data={'name':'microcentrifuge', "min_time": 1, "time_units": 'sec'})
        # comp2 = Component(self.protocol, parent=action1)
        self.protocol.save()
        self.protocol.delete_node(machine1['objectid'])
        self.protocol.save() #5 / 0

        history = self.protocol.history_set.all()
        for h in history:
            print "\nHISTORY EVENT: %d" % h.pk
            pp.pprint( h.data )

        self.assertEquals(len(history[3].data['update']), 1)                # LOG THE PUBLISH CHANGE
        self.assertEquals(history[3].data['create'][0]['type'], 'step')     # STEP SHOULD SHOW UP AS A CREATION
        self.assertEquals(history[2].data['create'][0]['type'], 'action')
        
        # TESTS FOR ADDING A MACHINE TO AN ACTION
        self.assertEquals(history[1].data['create'][0]['type'], 'machine')
    
        # TEST THAT MACHINE IS BEING DELETED
        self.assertEquals(len(history[0].data['delete']), 1)
        self.assertEquals(history[0].data['delete'][0]['type'], 'machine')

            # TEST THAT DURATION IS GETTING UPDATED
        self.assertEquals(len(history[0].data['update']), 2)                
        self.assertIn('duration', history[0].data['update'][0]['attrs'])
        self.assertIn('duration', history[0].data['update'][1]['attrs'])







        
        
