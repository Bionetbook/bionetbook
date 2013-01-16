def findancestors(thing):
	''' specify and object (thing) to traceback, 
	returns G wich is an AGraph object
	to plot:
	G.draw('<filename>.svg/jpg/tiff/pdf', prog = 'dot')

	'''
	import pygraphviz as pgv

	mro = thing.__mro__
	base_relations = {}
	base_relations_literal = {}
	for i in mro:
		base_relations[i] = i.__bases__ 
		base_relations_literal[i.__name__] = [r.__name__ for r in base_relations[i]]
	# draw out main graph

	G = pgv.AGraph()
	G.node_attr['shape']='box'
	G.edge_attr['dir']='backward'
	G.edge_attr['arrowhead'] = 'normal'	
	G.graph_attr['rankdir']='BT'

	edges = []

	for i in base_relations:
		for k in base_relations[i]:
			edges.append((i.__name__,k.__name__))

	G.add_edges_from(edges)

	return G



