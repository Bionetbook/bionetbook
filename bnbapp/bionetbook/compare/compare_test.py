import pygraphviz as *
from protocols.models import Protocol

def compare_protocols(protocol_A,protocol_B):
	'''compare two protocols side by side
		both protocols come from the same template
		no complex diff, only layout
	'''
	import pygraphviz as *
	from protocols.models import Protocol
	
	reagent_verbs = ['add', 'combine']
	machine_verbs = ['heat', 'chill', 'centrifuge', 'spin']

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

	if verb is add or combine: 
		compare the reagent lists:








	'''
	




	# Start main loop:
	for i in NUM_ACTIONS:
		if actions_A[i][2] == actions_B[i][2]: # verb name is the same
			if actions_A[i][2] in reagent_verbs:
				rank = compare_reagents(actions_A[i], actions_B[i])
			if actions_A[i][2] in machine_verbs:
				rank = compare_machines(actions_A[i], actions_B[i])







def compare_reagents(location_A, location_B):

	# check if both have a component - list:
	a = protA.steps[location_A[0]]['actions'][location_A[1]]
	b = protB.steps[location_B[0]]['actions'][location_B[1]]
	if 'component - list' in a.keys() and 'component - 	list' in b.keys():
		# get components lists:
		ar = [a['component - list'][r]['reagent_name'] for r in range(len(a['component - list']))]
		br = [b['component - list'][r]['reagent_name'] for r in range(len(b['component - list']))]
		# compare reagent names
		diff_name = ar.symmetric_difference(br)
		same_name = ar.intersection(br)
		

			# compare reagent supplier
			# compare 
		# compare reagent concentrations
		# compare reagent volumes
		# compare reagent quantities

			







			










			# # find different keys():
			# a = set(protA.steps[actions_A[i][0]]['actions'][actions_A[i][1]].keys())
			# b = set(protB.steps[actions_B[i][0]]['actions'][actions_B[i][1]].keys())

			# if len(a.symmetric_difference(b)) == 0:
			# 	# no key difference, move to values difference
			# 	for i in a:
			# 		if type(a) ==unicode and type(b) == unicode:
			# 			if a[i] == b[i]


	


