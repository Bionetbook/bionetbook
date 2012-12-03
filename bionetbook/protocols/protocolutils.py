# helper functions for parsing the yaml protocol structure:
# Author: Oren Schaedel
# Version: 0.1
# date 12/Nov/2012

# this is list of helper funcitons for accessing a protocol:
__metaclass__ = type
import sys
import yaml
import math


class Protocol:
	def __init__(self, fname):
		stream = file(fname, 'r')
		self.yaml = yaml.load(stream)
		self.name = self.Yaml['Name']
		self.components = self.Yaml['components-location']
	 	self.specific_tags = self.Yaml['Specific_tags']
	 	self.doi = self.Yaml['Reference_DOI']
	 	self.url = self.Yaml['Reference_URL']
	 	self.ssteps = self.Yaml['steps'] # make this a summary option with keyword tags
	 	self.pmid = self.Yaml['Reference_PMID']
	 	self.input = self.Yaml['Input']
	 	self.remarks = self.Yaml['Remarks']
	 	self.output = self.Yaml['Output']
	 	self.category_tags = self.Yaml['Category_tags']
	 	# self.schedule_padded = 'None'
	 	# self.totaltime = 'None'
	 	

 	def get_name(self):
		return self.Name

	def get_num_steps(self):
 		self.num_steps = len(self.Yaml['steps'])
 		return self.num_steps

 	def get_num_actions(self):
 		self.num_actions = [len(s['Actions']) for s in self.steps]
 		return self.num_actions

 	def get_actions_by_step(self):
 	 	self.actions_by_Step = []
 	 	for stepnum in range(0, self.get_num_steps()):
			tmp = [self.steps[stepnum]['Actions'][r]['verb'] for r in range(0, self.get_num_actions()[stepnum])]
			self.actions_by_Step.append(tmp)
		return self.actions_by_Step

	def get_reagent_data(self, format):
		
		self.needed_reagents = []
		# check if there are components in the protocol:
		if self.components[0] > 0:
			if format == 'None':
				for l in self.Components: # l = [rownum, stepnum, actionnum]
					cur_list = self.steps[l[1]]['Actions'][l[2]]['component - list'] # list of reagents starting at stepnum(l[1]), actionnum(l[2])
					[self.needed_reagents.append(r) for r in cur_list]
			
			else:
				for l in self.Components: # l = [rownum, stepnum, actionnum]
					cur_list = [self.steps[l[1]]['Actions'][l[2]]['component - list'][r]['reagent_name'] for r in range(0, len(self.steps[l[1]]['Actions'][l[2]]['component - list']))]
					[self.needed_reagents.append(r) for r in cur_list]

		return self.needed_reagents

	def get_action_tree(self):
		self.action_tree = []
		for stepnum in range(0, self.get_num_steps()): # traversign all steps
			for actionnum in range(0, len(self.steps[stepnum]['Actions'])): # traversing all actions per step
				self.Action_tree.append([stepnum, actionnum, self.steps[stepnum]['Actions'][actionnum]['verb']])
		
		return self.action_tree		

	def get_tree_by_field(self, field):
		self.Tree_by_field = []
		for stepnum in range(0, self.get_num_steps()): # traversign all steps
			for actionnum in range(0, len(self.steps[stepnum]['Actions'])): # traversing all actions per step
				try:
					self.Tree_by_field.append([stepnum, actionnum, self.steps[stepnum]['Actions'][actionnum][field]])
				except KeyError:
					continue	
			
		return self.Tree_by_field	

	def get_reagent_price(self):
		pass

	def get_cum_price(self):
		pass

	def get_schedule_data(self):
		time_atts = ('verb','min_time','max_time','time_units','duration_comment')
		self.actions_sequence =[]
		# traversing all step and action nodes in the protocol:
		
		for stepnum in range(0, self.get_num_steps()): # traversign all steps
			for actionnum in range(0, len(self.steps[stepnum]['Actions'])): # traversing all actions per step
				tmp = {}
				# find the time related annotated field that this protcol has
				tagged_fields = [r for r in self.steps[stepnum]['Actions'][actionnum].keys() if r in time_atts]
				for l in tagged_fields: # insert the valid tagged_fields into a tmp dict
					tmp[l] = self.steps[stepnum]['Actions'][actionnum][l] 
				self.actions_sequence.append(tmp)	# append this action dict to the action_sequence list
		return self.actions_sequence
	
	def get_duration_by_line(self):
		# this function can be included in the Quality control after protocol entry.
		# User can enter unspecified times if they can estimate them. 

		self.schedule_line = []

		for line in self.get_schedule_data():

			out_line = [] 
			out_line.append(line['verb'])
			
			if 'min_time' in line:
				out_line.append(line['min_time'])

			if 'max_time' in line:
				out_line.append(line['max_time'])

			if 'time_units' in line:
				out_line.append(line['time_units'])
				
			if 'duration_comment' in line:
				out_line.append(line['duration_comment'])

			self.schedule_line.append(out_line) 

		return self.schedule_line

	def set_padding(self):

		# self.schedule_padded ='True'
		self.schedule_padding_list = [['pad', 1, 1, 'minutes', 'Active'] for r in range(0, len(self.get_duration_by_line()))]
		self.schedule_padded = []
		try:
			self.schedule_line
			for i in range(0, len(self.get_duration_by_line())):
				self.schedule_padded.append(self.get_duration_by_line()[i])
				self.schedule_padded.append(self.schedule_padding_list[i])
		except AttributeError:
			print 'get_duration_by_list before adding padding'		

		return self.schedule_padded		

	def get_duration(self, *args):
		
		if 'padding' in args:
			self.set_padding()
			schedule = self.schedule_padded
		else:
			self.get_duration_by_line()
			schedule = self.schedule_line
		active_list = []
		passive_list = []
		total_list= []
		for line in schedule:
			if type(line[1]) == int or line[1][0].isdigit():
				if line[3]=='minutes':
					total_list.append(float(line[1]))
				if line	[3]=='hours':
					total_list.append(float(line[1]*60))
				if line	[3]=='days':
					total_list.append(float(line[1]*60*24))
				if 'Active'.lower() in line[4].lower():
					active_list.append(total_list[-1])
				if 'Passive'.lower() in line[4].lower():
					passive_list.append(total_list[-1])		
			else:
				continue

		total_time = math.ceil(sum(total_list))
		d = divmod(math.ceil(total_time),60)
		pprint_total_time = '{0} hours and {1} minutes'.format(d[0], d[1])
		total_active_time = sum(active_list)			
		total_passive_time = sum(passive_list)	
		if 'literal' in args:
			return pprint_total_time
		else:
			return total_time*60 
	





	# 	for r in self.








	# return Protocol	 	





# if __name__ == '__main__': 		
# 	import sys
# 	import yaml

# 	fname = sys.argv[1]
# 	stream = file(fname, 'r')
# 	protocol = yaml.load(stream)
# 	class Protocol: pass

# 	Protocol.Name = protocol['Name']
# 	print Protocol.Name

	