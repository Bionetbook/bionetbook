# helper functions for parsing the yaml protocol structure:
# Author: Oren Schaedel
# Version: 0.1
# date 12/Nov/2012

# this is list of helper funcitons for accessing a protocol:

# import sys
# import yaml

# class Protocol(protocol):
# 		def __init__(self):
# 			Protocol.Name = protocol['Name']
# 			Protocol.Components = protocol['components-location']
# 		 	Protocol.Specific_tags = protocol['Specific_tags']
# 		 	Protocol.DOI = protocol['Reference_DOI']
# 		 	Protocol.URL = protocol['Reference_URL']
# 		 	Protocol.Steps = protocol['steps'] # make this a summary option with keyword tags
# 		 	Protocol.PMID = protocol['Reference_PMID']
# 		 	Protocol.Input = protocol['Input']
# 		 	Protocol.Remarks = protocol['Remarks']
# 		 	Protocol.Output = protocol['Output']
# 		 	Protocol.Category_tags = protocol['Category_tags']

# 	 	def get_num_steps(self):
# 	 		num_steps = len(protocol['steps'])
# 	 		return self.num_steps

if __name__ == '__main__': 		
	import sys
	import yaml

	fname = sys.argv[1]
	stream = file(fname, 'r')
	protocol = yaml.load(stream)
	class Protocol: pass

	Protocol.Name = protocol['Name']
	print Protocol.Name

	