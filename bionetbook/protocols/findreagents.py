# /usr/bin/python

# yamltonestedstruct
# this script checks if the yaml file is formatted correctly and unpacks into the nested structure


import yaml
import sys


fname = sys.argv[1]
stream = file(fname, 'r')

Protocol = yaml.load(stream)

# find all the reagents needed in the protocol and return as a list
needed = []

# check if there are components in the protocol:

if 'components-location' in prot.keys():
	for l in prot['components-location']: # l = [rownum, stepnum, actionnum]
		# local_list_len = range(0, len(prot['steps'][l[1]]['Actions'][l[2]]['component - list']))
		# print local_list_len
		cur_list = prot['steps'][l[1]]['Actions'][l[2]]['component - list'] # list of reagents starting at stepnum(l[1]), actionnum(l[2])
		[needed.append(r) for r in cur_list]

return needed

