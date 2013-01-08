import pygraphviz as *
from protocols.models import Protocol

def compare_protocols(protocol_A,protocol_B):
	'''compare two protocols side by side
		both protocols come from the same template
		no complex diff, only layout
	'''
	import pygraphviz as *
	from protocols.models import Protocol
	
	try:
		protA = Protocol.objects.get(name__icontains=protocol_A)
		protB = Protocol.objects.get(name__icontains=protocol_B)
	except: # fix to ObjectDoesNotExsist
		return 'not in DB, try again'

	# are the action trees identical?
	# confirm action_tree lengths before starting main compare loop:
	NUM_ACTIONS = len(protA.get_action_tree())
	
	actions_A = protA.get_action_tree()
	actions_B = protB.get_action_tree()
	if len(actionsA) == len (actionsB):
		continue
	else:
		return 'protocols dont have the same length'

	'''score is accumulated through the compare:
	If all action sequences are the same: actions = 1, else, actions = 0 will deal with later
	If all attribute keys per action are the same: attribute_keys = 1, else: attribute_keys = similar/total.
	If all attribute values pe action are the same: attribute_values = 1, else: attribute_values = similar/total. 
	if the verb of the action is the same, the output will look like
	[step_num, action_num, verb_a[objectid], verb_b[objectid], attribute_key_score, attribute_value_score]
	attribute compare:
	if all attribute_keys are the same:







	'''
	




	# Start main loop:
	for i in NUM_ACTIONS:
		if actions_A[i][2] == actions_B[i][2]: # verb name is the same
			# find different keys():
			a = set(protA.steps[actions_A[i][0]]['actions'][actions_A[i][1]].keys())
			b = set(protB.steps[actions_B[i][0]]['actions'][actions_B[i][1]].keys())

			if len(a.symmetric_difference(b)) == 0:
				# no key difference, move to values difference
				for i in a:
					if type(a) ==unicode and type(b) == unicode:
						if a[i] == b[i]


	


