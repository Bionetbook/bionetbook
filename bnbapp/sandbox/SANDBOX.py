SANDBOX	


	c.same_layer_objects = c.get_reagents_by_action()	
	c.same_layer_objects_lit = c.get_reagents_by_action('literal')	
	
	# define the subgraph with a dict that groups objects into a single rank 
c.rank_objects = {} 
for i in c.same_layer_objects:
	c.rank_objects[i] = []
	c.rank_objects[i].append(c.same_layer_objects[i][0])
	c.rank_objects[i].append(i)
	c.agraph.add_edges_from([(i, c.rank_objects[i][0]) for i in c.rank_objects])

	# build all subgraphs:
names=['a1','a2','a3','a4','a5','a6','a7'] # automate to protName_verb for pairwise comparisson
nc=0
for i in c.rank_objects:
	N = c.agraph.add_subgraph(c.rank_objects[i], name='%s'%(names[nc]), rank = 'same', rankdir='LR')
	nc+=1
	# label the nodes in the subgraph of the current layer:
	for i in c.rank_objects:
		n = c.agraph.get_node(c.rank_objects[i][0]) # get rank node that links to base node for each rank
		# e = c.agraph.get_edge(c.rank_objects[i][0], c.rank_objects[i][1]) # fix this
		v = c.same_layer_objects[i] # get a list of all nodes of this subgraph
		n.attr['shape'] = 'record'
		
		''' assemble the label:
		remove commas,  - done
		attach measurement units -not yet
		add kwargs here
		'''	
		label_assembly = []

		for k in range(len(v)): # rename all reagents in an action
			tmp = c.objectid2name(v[k], reagents=True, units=True)
			name = tmp['name'].replace(',','')
			units = tmp['units']
			label_assembly.append(name + ' ' + units)

		
		n.attr['label'] = '{' + ' | '.join(label_assembly) +'}'

for step in c.steps:
    result[step['objectid']] = step
    print step['objectid']
    for action in step['actions']:
        result[action['objectid']] = action
        print '-' + action['objectid']	
        if 'component - list' in action:
            for component in action['component - list']:
                result[component['objectid']] = component
                print '--' + component['objectid']		