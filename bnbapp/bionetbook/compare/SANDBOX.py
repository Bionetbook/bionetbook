	SANDBOX	

for idxa in a_actions:
	
	a_name = a.nodes[idxa]['verb']
	if 'machine' in a.nodes[idxa].keys():
		a_type = 'machine'
		a_child = a.nodes[idxa]['machine']['objectid']
	# if 'components' in a.nodes[idxa].keys():
	else: 
		if len(a.nodes[idxa]['components']) == 0:
			a_type = 'other'
			a_child = None

		else: 
			a_type = 'components'
			a_child = [r['objectid'] for r in a.nodes[idxa]['components']]
	
	a_parent = a.nodes[idxa].parent['objectid'] # pointer to the step object
	idx_of_a = a_actions.index(idxa)
	
	if idx_of_a == 0: 
		a_previous = None
		a_next = 1

	if idx_of_a == len(a_actions): 
		a_previous = len(a_actions)-1#, len(a_actions)-2]
		a_next = None

	else:
		a_previous = idx_of_a - 1#, idx_of_self - 2]
		a_next = idx_of_a + 1#, idx_of_self + 2]

	print (idxa, a_name, a_type, a_previous, a_next) 	
	
	for idxb in b_actions:

		b_name = b.nodes[idxb]['verb']
		
		if 'machine' in b.nodes[idxb].keys():
			b_type = 'machine'
			b_child = b.nodes[idxb]['machine']['objectid']
		else: 
			if len(b.nodes[idxb]['components']) == 0:
				b_type = 'other'
				b_child = None

			else: 
				b_type = 'components'
				b_child = None
		
		b_parent = b.nodes[idxb].parent['objectid'] # pointer to the step object
		idx_of_b = b_actions.index(idxb)
		
		if idx_of_b == 0: 
			b_previous = None
			b_next = 1#,2]	

		if idx_of_b == len(b_actions): 
			b_previous = len(b_actions) - 1  #, len(b_actions)-2]
			b_next = None

		else:
			b_previous = idx_of_b - 1#, idx_of_b - 2]
			b_next = idx_of_b + 1#, idx_of_b + 2]	

		print (idxb, b_name, b_type, b_previous, b_next)	

		#-------- >  LOGIC < ---------------					

		if a_name == b_name and a_type == b_type:
			edges = True
		else:
			edges = False

		if a.nodes[a_actions[a_previous]]['verb'] ==  b.nodes[b_actions[b_previous]]['verb']:
			previous = True
		else:
			previous = False

		if a.nodes[a_actions[a_next]]['verb'] ==  b.nodes[b_actions[b_next]]['verb']:
			next = True
		else:
			next = False	
		
		if edges == True and previous ==True and next == True:
			comparator.append([idxa, idxb, 3])

		if edges == True and previous == True:
			comparator.append([idxa, idxb, 0])

		if edges == True and next == True:
			comparator.append([idxa, idxb, 1])












	# add base of first protocol:

	# set node couter:
	node_counter = len(A)

	# add thicl colored line
	for i in range(1, len(A)):
		agraph.add_edge(A[i-1], A[i])
		n=agraph.get_node(A[i])
		n.attr['shape']='box'
		n.attr['label']= b.nodes[A[i]]['verb']

	n = agraph.get_node(agraph.nodes()[0])
	n.attr['shape']='box'
	n.attr['label']=a.nodes[A[0]]['verb']

	# add base of second protocol:
	for i in range(1, len(B)):
		agraph.add_edge(B[i-1], B[i])
		n=agraph.get_node(B[i])
		n.attr['shape']='box'
		n.attr['label']= b.nodes[B[i]]['verb']

	n = agraph.get_node(agraph.nodes()[node_counter])
	n.attr['shape']='box'
	n.attr['label']=b.nodes[B[0]]['verb']


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
	# !!! original !!!


		def add_layer(self, **kwargs):

			''' determines the way layer data is displayed on the plot:
			keys:
				layer: sets the data in the layer, values:
					- reagent: displayes the reagents layer.
					- machines: displays what machines are needed.
				display: sets the display options for the current layer, values:
					- compact: minimal information, for reagents 'name, conc, vol'
					- full: each object in the layer is node; each reagent is a node, each machine is a node. 



			'''
			
			# create base plot:
			if not self.agraph:
				self.plot()

			if not kwargs:
				return 'please add layer=reagents / schedule / machines / strains etc'

			# add a reagents layer: 
			if 'reagents' in kwargs.keys():	
				# find the nodes and edges that define the layer:
				self.same_layer_objects = self.get_reagents_by_action()	
				
				# define the subgraph with a dict that groups objects into a single rank 
				self.rank_objects = {} 
				for i in self.same_layer_objects:
						self.rank_objects[i] = []
						self.rank_objects[i].append(self.same_layer_objects[i][0])
						self.rank_objects[i].append(i)
					else:
						self.rank_objects[i] = self.same_layer_objects[i]
						self.rank_objects[i].append(i)
			
					self.agraph.add_edges_from([(i, self.rank_objects[i][0]) for i in self.rank_objects])

				# build all subgraphs:
				names=['a1','a2','a3','a4','a5','a6','a7'] # automate to protName_verb for pairwise comparisson
				nc=0
				for i in self.rank_objects:
					N = self.agraph.add_subgraph(self.rank_objects[i], name='%s'%(names[nc]), rank = 'same', rankdir='LR')
					nc+=1
				# label the nodes in the subgraph of the current layer:
				for i in self.rank_objects:
					n = self.agraph.get_node(self.rank_objects[i][0]) # get rank node that links to base node for each rank
					# e = self.agraph.get_edge(self.rank_objects[i][0], self.rank_objects[i][1]) # fix this
					v = self.get_reagents_by_action()[i] # get a list of all nodes of this subgraph
					n.attr['shape'] = 'record'
					
					''' assemble the label:
					remove commas,  - done
					attach measurement units -done
					add kwargs here
					'''	
					label_assembly = []

					for k in v: # rename all reagents in an action
						name = self.nodes[k]['name']
						label = self.nodes[k].label
						label_assembly.append(name + ' '  + label)

					
					n.attr['label'] = '{' + ' | '.join(label_assembly) +'}' # verticle display, for horizontal, remove "{}"
					
					'''n.attr['URL'] = '/Users/Oren/Coding/bionetbook/bnbapp/bionetbook/hex.svg'	 
					Import the slug system into this,
					'''











