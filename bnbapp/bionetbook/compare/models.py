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
				v = self.get_reagents_by_action()[i] # get a list of all nodes of this subgraph
				n.attr['shape'] = 'record'
				
				''' assemble the label:
				remove commas,  - done
				attach measurement units -done
				add kwargs here
				'''	
				label_assembly = []

				for k in v: # rename all reagents in an action
					# tmp = self.objectid2name(v[k], reagents=True, units=True)
					name = self.nodes[k]['name']
					label = self.nodes[k].label
					label_assembly.append(name + ' '  + label)

				
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



def compare2versions(protocol_A, Protocol_B, **kwargs):

	protocol_1 = ProtocolPlot.objects.get(name__icontains=protocol_A)	
	protocol_2 = ProtocolPlot.objects.get(name__icontains=Protocol_B)

	return protocol_1.name,protocol_2.name	





# def plotprotocol(protocol_name):
# 	prot = ProtocolPlot
# 	prot.setProtocol(protocol_name)
# 	return prot.plot()



# # def add_subgraph_machine(A):
# 	# identify machine steps:

	

# # Plot.draw('compare.svg', prog = 'dot')


# #TODO:
# '''
# turn into objects
# add urls and slugs'''


