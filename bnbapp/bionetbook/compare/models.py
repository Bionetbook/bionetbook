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

		# this goes to the view page:
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

		# EDGE_LIST - list of tuples that mark the parent and child nodes of the base graph
		# RANK_LIST - list of objects that are linked on the same rank - all edges are drawn out
		# LABEL-LIST - list of objects that will be added to label one node. needs another argument. 

		# This function takes in layer_data dict, which contains: 
			#keys - anchor_nodes ; the source from which a rank of a layer is generated. 
			#values - objectid of the child node; draws an attachment to the base diagram. 
			#if more than one value, then this is a reference to a mutli-labeled node in which a list or table 
			#of objectids for the other labels that appear on the keys child node. 
		
		# ----- This Section should stay here and it handles the layer logic ---------
		self.layer_data = {} 

		if 'machine' in kwargs and kwargs['machine']==True:

			MACHINE_VERBS = ['heat', 'chill', 'centrifuge', 'agitate', 'collect', 'cook', 'cool', 'electrophorese', 'incubate', 'shake', 'vortex']
			anchor_nodes = [self.nodes[r[2]]['objectid'] for r in self.get_action_tree('objectid') if self.nodes[r[2]]['verb'] in MACHINE_VERBS]
			self.layer_data = {} 
			for verb in anchor_nodes:
				self.layer_data[self.nodes[verb]['objectid']] = self.nodes[verb]['machine']['objectid'] 

			self.edges_list = [(i,j) for i,j in self.layer_data.items()]	

		if 'components' in kwargs and kwargs['components']==True:
			self.layer_data = self.get_reagents_by_action()	
			# define the subgraph with a dict that groups objects into a single rank 
			remapper = {}
			for k,v in self.layer_data.items():
				remapper[k] = v[0]		

			self.edges_list = [(i,j) for i,j in remapper.items()]	
		
	

	# ------- this should be moved to the compare.view page  --------------:
		
		self.agraph.add_edges_from(self.edges_list)
		
		
		# add all self.ranks that will be built together into one layer:

		# build all subgraphs: and label nodes
		
		for parent,child in self.edges_list:
			if 'multi_label' in kwargs and kwargs['multi_label']==True: # add this if you pass a dict but not a list of tuples
				rank_list = list(self.layer_data[parent])
				rank_list.append(parent)
			else:
				rank_list = (parent,child) 		
			
			N = self.agraph.add_subgraph(rank_list, rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))
			e = self.agraph.get_edge(parent,child)
			n = self.agraph.get_node(child) # get rank node that links to base node for each rank
			n.attr['shape'] = 'record'
			
			if 'what' in self.nodes[parent]:
				e.attr['label'] = self.nodes[parent]['what'] 

			if 'multi_label' in kwargs and kwargs['multi_label'] == True:
				label_assembly = []
 				items = self.layer_data[parent]
 				
				for v in items:
					name = self.nodes[v]['name']
					label = self.nodes[v].label
					label_assembly.append(name + ' '  + label)
					n.attr['label'] = '{' + ' | '.join(label_assembly) +'}'
			else:	
				n.attr['label'] = self.nodes[child].label	

	def remove_layer(self): #, layer_names):
		self.agraph.remove_nodes_from([(v) for k,v in self.edges_list])
		# [self.agraph.remove_subgraph(name=r) for r in layer_names]


	






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


