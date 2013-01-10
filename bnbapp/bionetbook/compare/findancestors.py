
def findancestors(thing):
	''' specify and object (thing) to traceback, 
	return G an AGraph object'''
	import pygraphviz as pgv

	mro = thing.__mro__
	bases = {}
	for i in mro:
		bases[i] = i.__bases__ # if I can capture the objectname and not a str of the object name. 

	# draw out main graph

	G = pgv.AGraph()
	G.node_attr['shape']='box'
	G.edge_attr['dir']='backward'
	G.edge_attr['arrowhead'] = 'normal'	
	G.graph_attr['rankdir']='BT'

	edges = []

	for i in bases:
		for k in bases[i]:
			edges.append((i.__name__,k.__name__))

	G.add_edges_from(edges)

	return G



