# getschedulingdata
# version 0.1
# created 11/12/2012
# author: Oren Schaedel

# this function takes a protocol and returns a list with actions formatted:
#[{},{}] each dict is an action
#{verb,min_time,max_time,active/passive,time_units,calendars}

import yaml
import sys


fname = sys.argv[1]
stream = file(fname, 'r')

protocol = yaml.load(stream)
actions_sequence = []
time_atts = ('verb','min_time','max_time','time_units','duration_comment')

# traversing all step and action nodes in the protocol:

for stepnum in range(0, len(protocol['steps'])): # traversign all steps
	for actionnum in range(0, len(protocol['steps'][stepnum]['Actions'])): # traversing all actions per step
		tmp = {}
		# find the time related annotated field that this protcol has
		tagged_fields = [r for r in protocol['steps'][stepnum]['Actions'][actionnum].keys() if r in time_atts]
		for l in tagged_fields: # insert the valid tagged_fields into a tmp dict
			tmp[l] = protocol['steps'][stepnum]['Actions'][actionnum][l] 
		actions_sequence.append(tmp)	# append this action dict to the action_sequence list

fname_new= fname[:fname.index('.')] + '_schedule.yaml'
stream = file(fname_new, 'w')
yaml.dump(actions_sequence, stream)
	