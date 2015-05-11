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



# loop through actions:
# find verb-type compatabilites
# determine what type of verb it is: component or machine. 
#   if both match verb - type make a dim connector add both to the same rank
# identifying an edge:
#  (a.nodes('oy38e9')['verb'],a.nodes('oy38e9')['verb'])


#    if they differ in key numbers, change the color of the square
#  compare both children:
# 	if they match, color both verbs in green 
#    if they dont, display both, with red highliting the diff and green the black the same
a.

a_actions = [r[2] for r in a.get_action_tree('objectid')] 
b_actions = [r[2] for r in b.get_action_tree('objectid')] 

comparator = []


for idxa in a_actions:
	# comparators:
	# name
	# type of child
	# younger brother 
	# older sister
	a_name = a.nodes[idxa]['verb']
	if 'machines' in a.nodes[idxa]['verb'].keys():
		a_type = 'machine'
		a_child = a.nodes[idxa]['machine']['objectid']
	else:
		a_type_comparator = 'components'
		a_child = a.nodes[idxa]['components']['objectid']	

	a_parent = a.nodes[idxa].parent['objectid'] # pointer to the step object
	idx_of_a = actions_a.index(idxa)
	
	if idx_of_a == 0: 
		a_previous = None
		a_next = 1

	# if idx_of_a == 1: 
	# 	a_previous = 0
	# 	a_next = [2,3]

	if idx_of_a == len(a_actions): 
		a_previous = len(a_actions)-1#, len(a_actions)-2]
		a_next = None

	# if idx_of_a == len(a_actions)-1: 
	# 	a_previous = [len(a_actions)-2, len(a_actions)-3]
	# 	a_next = idx_of_a +1	

	else:
		a_previous = idx_of_a - 1#, idx_of_self - 2]
		a_next = idx_of_a + 1#, idx_of_self + 2]

	for idxb in b_actions:

		b_name = a.nodes[idxb]['verb']
		
		if 'machines' in b.nodes[idxb]['verb'].keys():
			b_type = 'machine'
			b_child = b.nodes[idxb]['machine']['objectid']
		else:
			b_type_comparator = 'components'
			b_child = b.nodes[idxb]['components']['objectid']	

		b_parent = b.nodes[idxb].parent['objectid'] # pointer to the step object
		idx_of_b = b_actions.index(idxb)
		
		if idx_of_b == 0: 
			b_previous = None
			b_next = 1#,2]

		# if idx_of_b == 1: 
		# 	b_previous = 0
		# 	b_next = [2,3]	

		if idx_of_b == len(b_actions): 
			b_previous = len(b_actions)-1#, len(b_actions)-2]
			b_next = None

		# if idx_of_b == len(b_actions)-1: 
		# 	b_previous = [len(b_actions)-2, len(b_actions)-3]
		# 	b_next = idx_of_b +1	

		else:
			b_previous = idx_of_b - 1#, idx_of_b - 2]
			b_next = idx_of_b + 1#, idx_of_b + 2]						


		# compare the edge content:

		if a_name == b_name and a_type == b_type:
			edges = True
		else:
			edges = False

		#if a_type == b_type:
			# call an action to compare the contents of both. 	

		# comapre relatives: 
		if a.nodes[a_actions[a_previous]]['name'] ==  b.nodes[b_actions[b_previous]]['name']:
			previous = True
		else:
			previous = False

		if a.nodes[a_actions[a_next]]['name'] ==  b.nodes[b_actions[b_next]]['name']:
			next = True
		else:
			next = False	

		
		if edges == True and previous ==True and next == True:
			comparator.append([idxa, idxb, 3])

		if edges == True and previous == True:
			comparator.append([idxa, idxb, 0])

		if edges == True and next == True:
			comparator.append([idxa, idxb, 1])							