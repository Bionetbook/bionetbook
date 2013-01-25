from django.db import models

import pygraphviz as pgv 
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel

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



	def find_same_rank_objects_by_position(self, protocol_B):


		# a = ProtocolPlot.objects.get(name__icontains=protocol_A)	
		b = ProtocolPlot.objects.get(name__icontains=protocol_B)
		
		a_actions = [r[2] for r in self.get_action_tree('objectid')]
		b_actions = [r[2] for r in b.get_action_tree('objectid')]

	
		comparator = []

		for idxa in a_actions:
			
			a_name = self.nodes[idxa]['verb']
			if 'machine' in self.nodes[idxa].keys():
				a_type = 'machine'
				a_child = self.nodes[idxa]['machine']['objectid']
			# if 'components' in self.nodes[idxa].keys():
			else: 
				if 'components' not in self.nodes[idxa] or len(self.nodes[idxa]['components']) == 0:
					a_type = 'other'
					a_child = None

				else: 
					a_type = 'components'
					a_child = [r['objectid'] for r in self.nodes[idxa]['components']]
			
			a_parent = self.nodes[idxa].parent['objectid'] # pointer to the step object
			idx_of_a = a_actions.index(idxa)
			
			if idx_of_a == 0: 
				a_previous = self.nodes[idxa]['objectid']
				a_nextt = self.nodes[a_actions[idx_of_a + 1]]['objectid']

			if idx_of_a == len(a_actions)-1: 
				a_previous = self.nodes[a_actions[idx_of_a - 1]]['objectid']
				a_nextt = self.nodes[a_actions[idx_of_a]]['objectid']

			else:
				a_previous = self.nodes[a_actions[idx_of_a -1 ]]['objectid']
				a_nextt = self.nodes[a_actions[idx_of_a +1 ]]['objectid']

			# print (idxa, a_name, a_type, a_previous, a_nextt) 	
			
			for idxb in b_actions:

				b_name = b.nodes[idxb]['verb']
				
				if 'machine' in b.nodes[idxb].keys():
					b_type = 'machine'
					b_child = b.nodes[idxb]['machine']['objectid']
				else: 
					if 'components' not in b.nodes[idxb] or len(b.nodes[idxb]['components']) == 0:
						b_type = 'other'
						b_child = None

					else: 
						b_type = 'components'
						b_child = None
				
				b_parent = b.nodes[idxb].parent['objectid'] # pointer to the step object
				idx_of_b = b_actions.index(idxb)
				
				if idx_of_b == 0: 
					b_previous = b.nodes[b_actions[idx_of_b]]['objectid']
					b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

				if idx_of_b == len(b_actions)-1: 
					b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
					b_nextt = b.nodes[b_actions[idx_of_b ]]['objectid']

				else:
					b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
					b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

				# print (idxb, b_name, b_type, b_previous, b_nextt)	

				#-------- >  LOGIC < ---------------					

				if a_name == b_name and a_type == b_type:
					edges = True
				else:
					edges = False

				if self.nodes[a_previous]['verb'] ==  b.nodes[b_previous]['verb']:
					previous = True
				else:
					previous = False

				if self.nodes[a_nextt]['verb'] ==  b.nodes[b_nextt]['verb']:
					nextt = True
				else:
					nextt = False	
				
				if edges == True and previous ==True and nextt == True:
					comparator.append([idxa, idxb, 3])


		return comparator








	





	# plot both protocols as the same graph with a separate list of ndoes, use the pk attribute to draw them out. 


			# loop through actions:


	# find verb-type compatabilites
	# determine what type of verb it is: component or machine. 
	#   if both match verb - type make a dim connector add both to the same rank
		## create a list with [(pk_A, pk_B), 'identical', 'different_keys', 'different_values', url to the same graph with details ]
	#    if they differ in key numbers, change the color of the square
	#  compare both children:
	# 	if they match, color both verbs in green 
	#    if they dont, display both, with red highliting the diff and green the black the same
