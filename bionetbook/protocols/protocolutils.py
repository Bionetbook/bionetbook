# helper functions for parsing the yaml protocol structure:
# Author: Oren Schaedel
# Version: 0.1
# date 12/Nov/2012

# this is list of helper funcitons for accessing a protocol:
__metaclass__ = type
import sys
import yaml

class Protocol:
	def __init__(self, fname):
		stream = file(fname, 'r')
		self.Yaml = yaml.load(stream)
		self.Name = self.Yaml['Name']
		self.Components = self.Yaml['components-location']
	 	self.Specific_tags = self.Yaml['Specific_tags']
	 	self.DOI = self.Yaml['Reference_DOI']
	 	self.URL = self.Yaml['Reference_URL']
	 	self.Steps = self.Yaml['steps'] # make this a summary option with keyword tags
	 	self.PMID = self.Yaml['Reference_PMID']
	 	self.Input = self.Yaml['Input']
	 	self.Remarks = self.Yaml['Remarks']
	 	self.Output = self.Yaml['Output']
	 	self.Category_tags = self.Yaml['Category_tags']
	 	self.Schedule_padding = 'None'
	 	# future - add a pad finding detector.

 	def get_name(self):
		return self.Name

	def get_num_steps(self):
 		self.num_steps = len(self.Yaml['steps'])
 		return self.num_steps

 	def get_num_actions(self):
 		self.num_actions = [len(self.Steps[r]['Actions']) for r in range(0, self.get_num_steps())]  
 		return self.num_actions

 	def get_actions_by_step(self):
 	 	self.actions_by_Step = []
 	 	for stepnum in range(0, self.get_num_steps()):
			tmp = [self.Steps[stepnum]['Actions'][r]['verb'] for r in range(0, self.get_num_actions()[stepnum])]
			self.actions_by_Step.append(tmp)
		return self.actions_by_Step

	def get_reagent_data(self, format):
		
		self.needed_reagents = []
		# check if there are components in the protocol:
		if self.Components[0] > 0:
			if format == 'None':
				for l in self.Components: # l = [rownum, stepnum, actionnum]
					cur_list = self.Steps[l[1]]['Actions'][l[2]]['component - list'] # list of reagents starting at stepnum(l[1]), actionnum(l[2])
					[self.needed_reagents.append(r) for r in cur_list]
			
			else:
				for l in self.Components: # l = [rownum, stepnum, actionnum]
					cur_list = [self.Steps[l[1]]['Actions'][l[2]]['component - list'][r]['reagent_name'] for r in range(0, len(self.Steps[l[1]]['Actions'][l[2]]['component - list']))]
					[self.needed_reagents.append(r) for r in cur_list]

		return self.needed_reagents

	def get_action_tree(self):
		self.Action_tree = []
		for stepnum in range(0, self.get_num_steps()): # traversign all steps
			for actionnum in range(0, len(self.Steps[stepnum]['Actions'])): # traversing all actions per step
				tmp = []
				tmp.append([stepnum, actionnum, self.Steps[stepnum]['Actions'][actionnum]['verb']])
			self.Action_tree.append(tmp)
		return self.Action_tree		
# !!!!!!!!! this is where I left off !!!!!!!!!!!!!!!!!!!!!!			

		


	def get_reagent_price(self):
		pass

	def get_cum_price(self):
		pass

	def get_schedule_data(self):
		time_atts = ('verb','min_time','max_time','time_units','duration_comment')
		self.actions_sequence =[]
		# traversing all step and action nodes in the protocol:
		
		for stepnum in range(0, self.get_num_steps()): # traversign all steps
			for actionnum in range(0, len(self.Steps[stepnum]['Actions'])): # traversing all actions per step
				tmp = {}
				# find the time related annotated field that this protcol has
				tagged_fields = [r for r in self.Steps[stepnum]['Actions'][actionnum].keys() if r in time_atts]
				for l in tagged_fields: # insert the valid tagged_fields into a tmp dict
					tmp[l] = self.Steps[stepnum]['Actions'][actionnum][l] 
				self.actions_sequence.append(tmp)	# append this action dict to the action_sequence list
		return self.actions_sequence
	
	def get_duration(self):
		# this function can be included in the Quality control after protocol entry.
		# User can enter unspecified times if they can estimate them. 

		self.Schedule_line = []

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

			self.Schedule_line.append(out_line) 

		return self.Schedule_line

	def set_padding(self):

		self.Schedule_padding ='True'
		self.Schedule_padding_list = [['pad', 1, 1, 'minutes', 'Active'] for r in range(0, len(self.get_duration()))]
		self.Schedule_padded = []
		try:
			self.Schedule_line
			for i in range(0, len(self.get_duration())):
				self.Schedule_padded.append(self.get_duration()[i])
				self.Schedule_padded.append(self.Schedule_padding_list[i])
		except AttributeError:
			print 'get_duration before adding padding'		

		return self.Schedule_padded		


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

	