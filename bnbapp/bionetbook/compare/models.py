from django.db import models


from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel


def plot_base_protocol(protocol_name, **kvargs):
	class Plot:
		pass

	from protocols.models import Protocol, Action, Step
	import pygraphviz as pgv 
	try:
		Plot.prot = Protocol.objects.get(name__icontains=protocol_name)
	except: # fix to ObjectDoesNotExsist
		return 'not in DB, try again'

	Plot.G = pgv.AGraph()
	Plot.action_tree  = Plot.prot.get_action_tree('objectid')
	
	# Define graph node and edge attributes:
	
	Plot.G.node_attr['shape']='square'
	Plot.G.edge_attr['dir']='forward'
	Plot.G.edge_attr['arrowhead'] = 'normal'
	for i in range(1, sum(Plot.prot.get_num_actions())):
	    Plot.G.add_edge(Plot.action_tree[i-1][2],Plot.action_tree[i][2])
	    n=Plot.G.get_node(Plot.action_tree[i][2])
	    n.attr['shape']='box'
	    n.attr['label']= "%s"%(Plot.prot.get_action_tree()[i][2])

	n = Plot.G.get_node(Plot.G.nodes()[0])
	n.attr['shape']='box'
	n.attr['label']=Plot.prot.get_action_tree()[0][2]

	if kvargs and kvargs['layout'] == 'blocks':
		Plot.G.edge_attr['arrowhead']='none'
		Plot.G.edge_attr['color']='white'

	return Plot
	
def add_subgraph_reagent(Plot, **kvargs):

	# Getting a list of reagent->verb objectid mapping
	
	Plot.reagent_verb_edges = Plot.prot.get_reagent_data('objectid')
	Plot.G.add_edges_from(Plot.reagent_verb_edges)
	Plot.verb_reagent_oid = Plot.prot.get_reagents_by_action()
	# concatenate verb to reagents for subgraph build:
	[Plot.verb_reagent_oid[i].append(i) for i in Plot.verb_reagent_oid]
	# build all subgraphs:
	names=['a1','a2','a3','a4','a5','a6','a7'] # automate to protName_verb for pairwise comparisson
	nc=0
	for i in Plot.verb_reagent_oid:
		N = Plot.G.add_subgraph(Plot.verb_reagent_oid[i], name='%s'%(names[nc]), rank = 'same', rankdir='LR')
		N.graph_attr['rank']='same'
		N.graph_attr['rankdir']='LR'
		nc+=1

	# set attributes for edges in reagent subgraph:
	for i in range(len(Plot.reagent_verb_edges)):
		n = Plot.G.get_edge(Plot.reagent_verb_edges[i][0],Plot.reagent_verb_edges[i][1])
		n.attr['arrowhead'] = 'empty'
		n.attr['style'] = 'dashed'

	# set attributes of nodes in reagent subgraph:
	Plot.reagents = Plot.prot.get_reagent_data('name_objectid')
	for i in Plot.reagents:
		n = Plot.G.get_node(i[1])
		n.attr['label'] = "%s"%(i[0])
		n.attr['shape'] = 'rectangle'
		# n.attr['URL'] = '/Users/Oren/Coding/bionetbook/bnbapp/bionetbook/hex.svg'

	if kvargs and kvargs['layout']=='neat':
		'''
		figure out how to render the subgraph on the right side of the main graph 
		add the record with automatic reagent naming



		'''

	return Plot 

# def add_subgraph_machine(A):
	# identify machine steps:

	

# Plot.draw('compare.svg', prog = 'dot')


#TODO:
'''
turn into objects
add urls and slugs'''










