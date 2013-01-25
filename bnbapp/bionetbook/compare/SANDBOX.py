	SANDBOX	


	# add base of first protocol:

	# set node couter:
node_counter = len(A)

	# add thicl colored line
for i in range(1, len(A)):
	agraph.add_edge(A[i-1], A[i])
	n=agraph.get_node(A[i])
	n.attr['shape']='box'
	n.attr['label']= a.nodes[A[i]]['verb'] + '_' + a.nodes[A[i]]['objectid']

n = agraph.get_node(agraph.nodes()[0])
n.attr['shape']='box'
n.attr['label']=a.nodes[A[0]]['verb'] + '_' + a.nodes[A[0]]['objectid']

	# add base of second protocol:
for i in range(1, len(B)):
	agraph.add_edge(B[i-1], B[i])
	n=agraph.get_node(B[i])
	n.attr['shape']='box'
	n.attr['label']= b.nodes[B[i]]['verb'] + '_' + b.nodes[B[i]]['objectid']

n = agraph.get_node(agraph.nodes()[node_counter])
n.attr['shape']='box'
n.attr['label']=b.nodes[B[0]]['verb'] + '_' + b.nodes[B[0]]['objectid']


	# add first protocool layer

	MACHINE_VERBS = ['heat', 'chill', 'centrifuge', 'agitate', 'collect', 'cook', 'cool', 'electrophorese', 'incubate', 'shake', 'vortex']
	anchor_nodes = [a.nodes[r[2]]['objectid'] for r in a.get_action_tree('objectid') if a.nodes[r[2]]['verb'] in MACHINE_VERBS]
	a.layer_data = {} 
	for verb in anchor_nodes:
		a.layer_data[a.nodes[verb]['objectid']] = a.nodes[verb]['machine']['objectid'] 

	a.edges_list = [(i,j) for i,j in a.layer_data.items()]	

	agraph.add_edges_from(a.edges_list)

	for parent,child in a.edges_list:
		
		rank_list = (parent,child) 		
		N = agraph.add_subgraph(rank_list, rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))
		e = agraph.get_edge(parent,child)
		n = agraph.get_node(child) # get rank node that links to base node for each rank
		n.attr['shape'] = 'record'
		
		if 'what' in a.nodes[parent]:
			e.attr['label'] = a.nodes[parent]['what'] 

		n.attr['label'] = a.nodes[child].label


	# Specify the second graph layer:

	anchor_nodes_b = [b.nodes[r[2]]['objectid'] for r in b.get_action_tree('objectid') if b.nodes[r[2]]['verb'] in MACHINE_VERBS]
	b.layer_data = {} 
	for verb in anchor_nodes_b:
		b.layer_data[b.nodes[verb]['objectid']] = b.nodes[verb]['machine']['objectid'] 

	b.edges_list = [(i,j) for i,j in b.layer_data.items()]	

	agraph.add_edges_from(b.edges_list)

	for parent,child in b.edges_list:
		
		rank_list = (parent,child) 		
		N = agraph.add_subgraph(rank_list, rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))
		e = agraph.get_edge(parent,child)
		n = agraph.get_node(child) # get rank node that links to base node for each rank
		n.attr['shape'] = 'record'
		
		if 'what' in b.nodes[parent]:
			e.attr['label'] = b.nodes[parent]['what'] 

		n.attr['label'] = b.nodes[child].label





	# ________________________________________________
	
def find_children_similarities(self, comparators):

# filtering the first list of lists:

# find the objects that appear more than once

mappings = {}
for i in out1:
    if i[0] not in mappings:
        mappings[i[0]] = []
        mappings[i[0]].append(i[1])
    else:
        mappings[i[0]].append(i[1])

uniq = dict((k,v) for k,v in mappings.items() if len(v)>1)



# content filter:
matches = []

for ref,options in uniq.items():
	if 'machine' in a.nodes[ref].keys():
		for candidate in options:
			if 'machine' in b.nodes[candidate].keys():
				d = DictDiffer(a.nodes[ref]['machine'],b.nodes[candidate]['machine'])
				# print [ref, candidate, d.added(), d.removed(), d.changed()]
				tmp = [ref,candidate, len(d.added()) + len(d.removed()) + len(d.changed())]
				matches.append(tmp)



	# there are 3 loops here on purpose, machines and components have different children issues		

for ref,options in uniq.items():
	if 'components' in a.nodes[ref].keys():
		for candidate in options:
			if 'components' in b.nodes[candidate].keys():
				d = DictDiffer(a.nodes[ref]['components'],b.nodes[candidate]['components'])
				print [ref, candidate, d.added(), d.removed(), d.changed()]

# !!! ---------  > finish writing this wrpapper for the DictDiffer and diff methods < -------!!!!!!!!

# make a data model that can accept the differnces and pass them on to the pygraphviz data model .



# Find the rows where matching 1 neighbor isnt enough:

# find the edges that need to be ranked:
a_s = [r[0] for r in comparators]
b_s = [r[1] for r in comparators]

a_uniques = [ x for x in a_s if a_s.count(x) == 1]
a_diffs = [ x for x in a_s if a_s.count(x) > 1]

b_uniques = [ x for x in b_s if b_s.count(x) == 1]
b_diffs = [ x for x in b_s if b_s.count(x) > 1]

a_uniq_in_comparator = [a_s.index(r) for r in a_uniques]
b_uniq_in_comparator = [b_s.index(r) for r in b_uniques]

if len(set(a_uniq_in_comparator)-set(b_uniq_in_comparator)):
	diffs = list(set(range(len(comparators)))- set(a_uniq_in_comparator))
	diff = [comparators[r] for r in diffs]


[u'adrmwt', u'lk1yt0', 5],
[u'adrmwt', u'i7w4wg', 5],
# 1 [u'adrmwt', u'8v7w7q', 0],

[u'bavsb0', u'lk1yt0', 4],
[u'bavsb0', u'i7w4wg', 0],
# 2 [u'bavsb0', u'8v7w7q', 5],

[u'kbzqcb', u'd6m0hh', 0],
[u'kbzqcb', u'nwv41j', 0],

[u'thfavi', u'd6m0hh', 0],
[u'thfavi', u'nwv41j', 0]


















				else:
					# they are the same length, 
					# send to compare machine / component function, 
					# score 10 for perfect match
					# score 9 for one mismach
					# score 8 for 2 mismatches
					# etc. 
					# return the labels that have to be colored differntly. 




# determine if they have the same number of children
# determine thier children keys match. 
# determine if the valuse of the children match. 







class DictDiffer(object):
	"""
	Calculate the difference between two dictionaries as:
	(1) items added
	(2) items removed
	(3) keys same in both but changed values
	(4) keys same in both and unchanged values
	"""
	def __init__(self, current_dict, past_dict):
		self.current_dict, self.past_dict = current_dict, past_dict
		self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
		self.intersect = self.set_current.intersection(self.set_past)
	def added(self):
		return list(self.set_current - self.intersect)
	def removed(self):
		return list(self.set_past - self.intersect)
	def changed(self):
		delta = list(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
		if 'name' in delta:
			delta.pop(delta.index('name'))
		if 'objectid' in delta:
			delta.pop(delta.index('objectid'))
		if 'slug' in delta:
			delta.pop(delta.index('slug'))
		return delta
	def unchanged(self):
		return list(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


