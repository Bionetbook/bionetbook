from django.db import models

import pygraphviz as pgv 
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel
from compare.utils import set_html_label, add_html_cell, merge_table_pieces

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
	def changed(self, **kwargs):
		delta = list(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
		if 'name' in delta and 'name' in kwargs:
			delta.pop(delta.index('name'))
		if 'objectid' in delta and 'objectid' in kwargs:
			delta.pop(delta.index('objectid'))
		if 'slug' in delta and 'slug' in kwargs:
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
		
		

		# this goes to the view page:
		self.agraph.node_attr['shape']='square'
		self.agraph.edge_attr['dir']='forward'
		self.agraph.edge_attr['arrowhead'] = 'normal'
		for i in range(1, sum(self.get_actions)):
		    self.agraph.add_edge(self.get_actions[i-1],self.get_actions[i])
		    n=self.agraph.get_node(self.get_actions[i])
		    n.attr['shape']='box'
		    n.attr['label']= "%s"%(self.get_actions[i])

		n = self.agraph.get_node(self.agraph.nodes())
		n.attr['shape']='box'
		n.attr['label']=self.get_actions[0]
		
		

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
			anchor_nodes = [self.nodes[r]['objectid'] for r in self.get_actions if self.nodes[r]['verb'] in MACHINE_VERBS]
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

	def same_rank_objects_by_1st_degree_nbrs(self, protocol_B):


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



class Compare(object):
	def __init__(self,protocol_a, protocol_b, **kwargs):
		import pygraphviz as pgv
		self.agraph = pgv.AGraph()
		self.protocol_A = protocol_a
		self.protocol_B = protocol_b
		self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions] # list of actions in pk-objectid format
		self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]

		# Draw out some control elements:
		# self.agraph.add_nodes_from(['add_common_actions_details',  )
		# cntrl = 





		# line up matching verbs in the same rank
		# we will add to this function more sophisticated things in the future.

		self.matching_verbs_pk = zip(self.A_pk,self.B_pk)
		self.matching_verbs = zip(self.protocol_A.get_actions, self.protocol_B.get_actions)

	def draw_two_protocols(self):
		
		# set node couter:
		node_counter = len(self.protocol_A.get_actions)
		
			# add thicl colored line
		for i in range(1, len(self.A_pk)):
			self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
			e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
			e.attr['style'] = 'setlinewidth(6)' 
			e.attr['color'] = '#B82F3' 
			n=self.agraph.get_node(self.A_pk[i])
			n.attr['shape']='box'
			n.attr['style'] = 'rounded'
			n.attr['label']= self.protocol_A.nodes[self.protocol_A.get_actions[i]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[i]].pk

		# Set the 0'th node in  protocol_A	
		n = self.agraph.get_node(self.matching_verbs_pk[0][0])
		n.attr['shape']='box'
		n.attr['style'] = 'rounded'
		n.attr['label']=self.protocol_A.nodes[self.protocol_A.get_actions[0]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[0]].pk

				# add base of second protocol:
		for i in range(1, len(self.B_pk)):
			self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
			n=self.agraph.get_node(self.B_pk[i])
			e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
			e.attr['style'] = 'setlinewidth(6)' 
			e.attr['color'] = '#015666' 
			n.attr['shape']='box'
			n.attr['style'] = 'rounded'
			n.attr['label']= self.protocol_B.nodes[self.protocol_B.get_actions[i]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[i]].pk

		# Set the 0'th node in  protocol_A	
		n = self.agraph.get_node(self.matching_verbs_pk[0][1])
		n.attr['shape']='box'
		n.attr['style'] = 'rounded'
		n.attr['label']=self.protocol_B.nodes[self.protocol_B.get_actions[0]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[0]].pk
		

		# create the pairwise - verb comparison and return a list of tuples for each verb_a: verb_b match. 

		for parent,child in self.matching_verbs_pk:
		
			rank_list = (parent,child) 		
			N = self.agraph.add_subgraph(rank_list, rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))
			N.edge_attr['color'] = 'white'

		return self.agraph

	def add_diff_layer(self, object_sorting = 'least_errors'):
		''' this function assumes that the pairs of objects are equivalent in that both have validated:
			'machines'
			'components'
			'''
		for verb_a,verb_b in self.matching_verbs: #[(node_a, node_b), ]

			if 'machine' in self.protocol_A.nodes[verb_a].keys():  # object has only one child:
				x = self.protocol_A.nodes[verb_a]['machine'].summary
				y = self.protocol_B.nodes[verb_b]['machine'].summary
				d = DictDiffer (x, y)
				# trigger = len(d.added()) + len(d.removed()) + len(d.changed(name = True, objectid = True, slug = True))
				# if trigger > 0:
					
				# --->  create a compare object that will apear between the 2 base diagrams:
				diff_object = self.protocol_A.nodes[verb_a]['machine'].pk
				ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
				eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)

				# set all diff objects on same rank:
				N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc])) 
				
				# set layout and colors
				s = self.agraph.get_node(diff_object)
				s.attr['shape'] = 'box'
				s.attr['color'] = '#C0C0C0'
				s.attr['style'] = 'rounded'

				# set label:
				s.attr['label'] = set_html_label(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), machine = True) 
				
				# --->

			if 'components' in self.protocol_A.nodes[verb_a].keys(): # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
				# Validate that reagent objectids are the same:


				if len(self.protocol_A.nodes[verb_a]['components']) ==0:
					continue

				else:
					components_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
					components_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
					
					components_list_diff = set(r['objectid'] for r in self.protocol_A.nodes[verb_a].children) - set(r['objectid'] for r in self.protocol_B.nodes[verb_b].children)

					if components_list_diff:
						pass
					
					else:
						scores = [] # tracks the error rate of a matching components
						content = [] # gets the html strings
						for m,n in zip(components_a,components_b): 
							d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
							scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
							# print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
							tmp = set_html_label(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), components = True) 
							# print tmp
							# print '\n'
							_name = add_html_cell(self.protocol_A.nodes[m]['name']) 
							content.append('<TR>' + _name + tmp)
							

					# if len(content) > 1:
					# 	rows = zip(scores, content)	
					# 	if 'object_sorting' == 'most errors':
					# 		rows_sorted = rows.sort().reversed()
					# 	else:
					# 		rows_sorted = rows.sort()

					# 	content_sorted = [r[1] for r in rows_sorted]	

					# else:
					# 	content_sorted = content	
					content_sorted  = content

						
					# set the base_graph node:
					diff_object = self.protocol_A.nodes[components_a[0]].pk	
					ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
					eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)		
					N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc])) 
					
					# set layout and colors
					s = self.agraph.get_node(diff_object)
					s.attr['shape'] = 'box'
					s.attr['color'] = '#C0C0C0'
					s.attr['style'] = 'rounded'
					s.attr['label'] = merge_table_pieces(content_sorted)
					


		return self.agraph			



def test_compare():
	a  = ProtocolPlot.objects.get(id='3')
	b  = ProtocolPlot.objects.get(id='19')
	G    = Compare(a,b)
	ag  = G.draw_two_protocols()
	af = G.add_diff_layer()
	af.draw('compare/Figures/test.svg', prog = 'dot')
	print 'no errors'
	







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
