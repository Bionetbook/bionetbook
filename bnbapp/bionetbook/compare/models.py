from django.db import models

import pygraphviz as pgv 
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel

class ProtocolPlot(Protocol):

	class Meta:	
		proxy = True

	def __init__(self, *args, **kwargs):
		super(ProtocolPlot, self).__init__(*args, **kwargs)
	
		self.agraph = pgv.AGraph()  # change all the Plot.G. to agraph. 	

	def plot(self, **kwargs):
		# super(ProtocolPlot, self).__init__(**kwargs)
		# self.prot = Protocol.objects.get(name__icontains=protocol_name)
		
		action_tree  = self.get_action_tree('objectid')
		self.agraph.node_attr['shape']='square'
		self.agraph.edge_attr['dir']='forward'
		self.agraph.edge_attr['arrowhead'] = 'normal'
		for i in range(1, sum(self.get_num_actions())):
		    self.agraph.add_edge(action_tree[i-1][2],action_tree[i][2])
		    n=self.agraph.get_node(action_tree[i][2])
		    n.attr['shape']='box'
		    n.attr['label']= "%s"%(self.get_action_tree()[i][2])

		n = self.agraph.get_node(self.agraph.nodes()[0])
		n.attr['shape']='box'
		n.attr['label']=self.get_action_tree()[0][2]
		
		

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
			self.same_layer_objects_lit = self.get_reagents_by_action('literal')	
			
			# define the subgraph with a dict that groups objects into a single rank 
			self.rank_objects = {} 
			for i in self.same_layer_objects:
				if kwargs['layout'] == 'compact':
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
				v = self.same_layer_objects[i] # get a list of all nodes of this subgraph
				n.attr['shape'] = 'record'
				
				''' assemble the label:
				remove commas,  - done
				attach measurement units -not yet
				add kwargs here
				'''	
				label_assembly = []

				for k in range(len(v)): # rename all reagents in an action
					tmp = self.objectid2name(v[k], reagents=True, units=True)
					name = tmp['name'].replace(',','')
					units = tmp['units']
					label_assembly.append(name + ' ' + units)

				
				n.attr['label'] = '{' + ' | '.join(label_assembly) +'}' # verticle display, for horizontal, remove "{}"
				
				'''n.attr['URL'] = '/Users/Oren/Coding/bionetbook/bnbapp/bionetbook/hex.svg'	 
				Import the slug system into this,
				'''

	def get_svg(self):
		self.agraph.layout('dot')
		return self.agraph

	def get_graph(self, agraph):
		agraph = self.agraph
		agraph.layout('dot')
		return agraph	



# def plotprotocol(protocol_name):
# 	prot = ProtocolPlot
# 	prot.setProtocol(protocol_name)
# 	return prot.plot()





# def plot_base_protocol(protocol_name, **kvargs):
# 	class Plot:
# 		pass

# 	from protocols.models import Protocol, Action, Step
# 	
# 	try:
# 		Plot.prot = Protocol.objects.get(name__icontains=protocol_name)
# 	except: # fix to ObjectDoesNotExsist
# 		return 'not in DB, try again'

# 	Plot.G = pgv.AGraph()
# 	Plot.action_tree  = Plot.get_action_tree('objectid')
	
# 	# Define graph node and edge attributes:
	
# 	Plot.G.node_attr['shape']='square'
# 	Plot.G.edge_attr['dir']='forward'
# 	Plot.G.edge_attr['arrowhead'] = 'normal'
# 	for i in range(1, sum(Plot.get_num_actions())):
# 	    Plot.G.add_edge(Plot.action_tree[i-1][2],Plot.action_tree[i][2])
# 	    n=Plot.G.get_node(Plot.action_tree[i][2])
# 	    n.attr['shape']='box'
# 	    n.attr['label']= "%s"%(Plot.get_action_tree()[i][2])

# 	n = Plot.G.get_node(Plot.G.nodes()[0])
# 	n.attr['shape']='box'
# 	n.attr['label']=Plot.get_action_tree()[0][2]

# 	if kvargs and kvargs['layout'] == 'blocks':
# 		Plot.G.edge_attr['arrowhead']='none'
# 		Plot.G.edge_attr['color']='white'

# 	return Plot
	
# def add_subgraph_reagent(Plot, **kvargs):

# 	# Getting a list of reagent->verb objectid mapping
	
# 	Plot.reagent_verb_edges = Plot.get_reagent_data('objectid')
# 	Plot.G.add_edges_from(Plot.reagent_verb_edges)
# 	Plot.verb_reagent_oid = Plot.get_reagents_by_action()
# 	# concatenate verb to reagents for subgraph build:
# 	[Plot.verb_reagent_oid[i].append(i) for i in Plot.verb_reagent_oid]
# 	# build all subgraphs:
# 	names=['a1','a2','a3','a4','a5','a6','a7'] # automate to protName_verb for pairwise comparisson
# 	nc=0
# 	for i in Plot.verb_reagent_oid:
# 		N = Plot.G.add_subgraph(Plot.verb_reagent_oid[i], name='%s'%(names[nc]), rank = 'same', rankdir='LR')
# 		N.graph_attr['rank']='same'
# 		N.graph_attr['rankdir']='LR'
# 		nc+=1

# 	# set attributes for edges in reagent subgraph:
# 	for i in range(len(Plot.reagent_verb_edges)):
# 		n = Plot.G.get_edge(Plot.reagent_verb_edges[i][0],Plot.reagent_verb_edges[i][1])
# 		n.attr['arrowhead'] = 'empty'
# 		n.attr['style'] = 'dashed'

# 	# set attributes of nodes in reagent subgraph:
# 	Plot.reagents = Plot.get_reagent_data('name_objectid')
# 	for i in Plot.reagents:
# 		n = Plot.G.get_node(i[1])
# 		n.attr['label'] = "%s"%(i[0])
# 		n.attr['shape'] = 'rectangle'
# 		# n.attr['URL'] = '/Users/Oren/Coding/bionetbook/bnbapp/bionetbook/hex.svg'

# 	if kvargs and kvargs['layout']=='neat':
# 		'''
# 		figure out how to render the subgraph on the right side of the main graph 
# 		add the record with automatic reagent naming



# 		'''

# 	return Plot 

# # def add_subgraph_machine(A):
# 	# identify machine steps:

	

# # Plot.draw('compare.svg', prog = 'dot')


# #TODO:
# '''
# turn into objects
# add urls and slugs'''


# # making the function a class with inheritance
# '''
# class ComponentBase(dict):
#     """Base class for the protocol components"""

#     keylist = ['name','objectid']

#     # ADD _meta CLASS TO USE SOME EXTRA DB-LIKE FUNCTIONALITY

#     class Meta:
#         def __init__(self, component):
#             self.component = component

#         def get_all_field_names(self):
#             result = self.component.keys()
#             result.sort()
#             return result

#     def __init__(self, protocol, data={}, **kwargs):
#         super(ComponentBase, self).__init__(**kwargs)

#         self.protocol = protocol

#         self['objectid'] = None #self.get_hash_id()
#         self['slug'] = None

#         self._meta = ComponentBase.Meta(self)

#         for item in self.keylist:       # REQUIRED ATTRIBUTES
#             self[item] = None

#         self.update_data(data)

#         if not 'name' in self or not self['name']:
#             self.set_name()

#     @property
#     def slug(self):
#         if not self['slug']:
#             self['slug'] = slugify(self['objectid'])
#         return self['slug']

#     def set_name(self):
#         self['name'] = self['slug']

#     def update_data(self, data={}, **kwargs):
#         for key in data:
#             self[key] = data[key]

#         #for item in kwargs:             # OVERRIDE DATA WITH ANY PARTICULAR KWARGS PASSED
#         #    self[item] = kwargs[item]

#     def __unicode__(self):
#         return self['slug']

#     @property
#     def title(self):
#         return self.protocol.name'''