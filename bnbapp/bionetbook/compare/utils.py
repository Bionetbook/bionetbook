def html_label_one_protocol(x, **kwargs):

	
	stack = []


	if 'machine' in kwargs:

		for i in x.keys():
			stack.append('<TR><TD color="#C0C0C0" colspan="2">%s</TD></TR>'%(x[i]))	

		return stack


	if 'components' in kwargs: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
		''' assuming that the objectids of the reagents are the same'''

		# count how many changes each reagent has, if 2 reagent names are different, write them last 
		_conc = ''
		_vol = ''
		_mass = ''

		if x['name'].lower() == 'total volume':
			_name = '<HR><TR><TD>%s</TD><TD>%s</TD></TR>'%(x['name'], str(x['vol'][0]) ) # + str(['vol'][1])

		# if 'conc' in changed:
		# 	_conc = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['conc'][0]) + str(x['conc'][1]), str(y['conc'][0]) + str(y['conc'][1]))  #<TD>%s</TD><TD>%s</TD>
		# 	# print 'CHANGED CONC'
		if 'conc' in x.keys():
			_conc = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['conc'][0]) + str(x['conc'][1])) #<TD colspan="2">%s</TD> 
			# print 'UNCHANGED CONC'
		

		# if 'vol' in changed and 'vol' not in unchanged:
		# 	_vol = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['vol'][0]) + str(x['vol'][1]), str(y['vol'][0]) + str(y['vol'][1])) #<TD>%s</TD><TD>%s</TD>
		if 'vol' in x.keys():
			_vol = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['vol'][0]) + str(x['vol'][1]))	#<TD colspan="2">%s</TD>


		# if 'mass' in changed and 'mass' not in unchaged:
		# 	_mass = '<TD color="#B82F3"><font color="#B82F3">%s</font>%</TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['mass'][0]) + str(x['mass'][1]), str(y['mass'][0]) + str(y['mass'][1])) # <TD>%s</TD><TD>%s</TD>
		if 'mass' in x.keys():
			_mass = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['mass'][0]) + str(x['mass'][1])) # <TD colspan="2">%s</TD>

		_name = '<TR><TD>%s</TD>' %x['name']

		return  _name + _vol + _conc + _mass + '</TR>'



def html_label_two_protocols(x,y,changed, unchanged, **kwargs):

	
	stack = []


	if 'machine' in kwargs:

		for i in changed:
			stack.append('<TR><TD color="#C0C0C0"><font color="#B82F3">%s</font></TD><TD color="#C0C0C0"><font color="#015666">%s</font></TD></TR>'%(x[i], y[i]))

		for j in unchanged:
			stack.append('<TR><TD color="#C0C0C0" colspan="2">%s</TD></TR>'%(x[j]))	

		return stack


	if 'components' in kwargs: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
		''' assuming that the objectids of the reagents are the same'''

		# count how many changes each reagent has, if 2 reagent names are different, write them last 
		_conc = ''
		_vol = ''
		_mass = ''

		# if x['name'].lower() == 'total volume':
		# 	_name = '<HR><TR><TD>%s</TD><TD>%s</TD></TR>'%(x['name'], str(x['vol'][0]) ) # + str(['vol'][1])

		if 'conc' in changed:
			_conc = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['conc'][0]) + str(x['conc'][1]), str(y['conc'][0]) + str(y['conc'][1]))  #<TD>%s</TD><TD>%s</TD>
			# print 'CHANGED CONC'
		if 'conc' in unchanged and 'conc' not in changed:
			_conc = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['conc'][0]) + str(x['conc'][1])) #<TD colspan="2">%s</TD> 
			# print 'UNCHANGED CONC'
		

		if 'vol' in changed and 'vol' not in unchanged:
			_vol = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['vol'][0]) + str(x['vol'][1]), str(y['vol'][0]) + str(y['vol'][1])) #<TD>%s</TD><TD>%s</TD>
		if 'vol' in unchanged and 'vol' not in changed:
			_vol = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['vol'][0]) + str(x['vol'][1]))	#<TD colspan="2">%s</TD>


		if 'mass' in changed and 'mass' not in unchaged:
			_mass = '<TD color="#B82F3"><font color="#B82F3">%s</font>%</TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['mass'][0]) + str(x['mass'][1]), str(y['mass'][0]) + str(y['mass'][1])) # <TD>%s</TD><TD>%s</TD>
		if 'mass' in unchanged and 'mass' not in unchanged:
			_mass = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['mass'][0]) + str(x['mass'][1])) # <TD colspan="2">%s</TD>

		_name = '<TR><TD>%s</TD>' %x['name']

		return  _name + _vol + _conc + _mass + '</TR>'

	if 'thermocycle' in kwargs: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
		''' assuming that the objectids of the reagents are the same'''

		# count how many changes each reagent has, if 2 reagent names are different, write them last 
		_temp = ''
		_time = ''
		_cycle = ''

		# if x['name'].lower() == 'total volume':
		# 	_name = '<HR><TR><TD>%s</TD><TD>%s</TD></TR>'%(x['name'], str(x['vol'][0]) ) # + str(['vol'][1])

		if 'temp' in changed:
			_temp = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['temp'][0]) + str(x['temp'][1]), str(y['temp'][0]) + str(y['temp'][1]))  #<TD>%s</TD><TD>%s</TD>
			# print 'CHANGED CONC'
		if 'temp' in unchanged and 'temp' not in changed:
			_temp = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['temp'][0]) + str(x['temp'][1])) #<TD colspan="2">%s</TD> 
			# print 'UNCHANGED CONC'
		

		if 'time' in changed and 'time' not in unchanged:
			_time = '<TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['time'][0]) + str(x['time'][1]), str(y['time'][0]) + str(y['time'][1])) #<TD>%s</TD><TD>%s</TD>
		if 'time' in unchanged and 'time' not in changed:
			_time = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['time'][0]) + str(x['time'][1]))	#<TD colspan="2">%s</TD>


		if 'cycle' in changed and 'cycle' not in unchaged:
			_cycle = '<TD color="#B82F3"><font color="#B82F3">%s</font>%</TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(' '.join( filter( None, x['cycle']) ), ' '.join(filter(None, y['cycle'])) ) # <TD>%s</TD><TD>%s</TD>
		if 'cycle' in unchanged and 'cycle' not in changed:
			_cycle = '<TD color="#C0C0C0" colspan="2">%s</TD>'%( ' '.join(filter(None, x['cycle'])) ) # <TD colspan="2">%s</TD>

		_name = '<TR><TD>%s</TD>' %x['name']

		return  _name + _temp + _time + _cycle + '</TR>'
	


def add_html_cell(m):
	return '<<font size = "20">%s</font>>'%(m)

def merge_table_pieces(content_tmp, layer = None):
	''' label is an HTML object and for automation sake, created by concatenating a few peices:
		table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">' --> defines the table properties in HTML
		content = '<TR><TD>{0}</TD><TD>{1}</TD></TR><TR><TD colspan="2">{2}</TD></TR>' --> generates the content of the comparison table
		merge = '<' + table + content + '</TABLE>>'	--> merges the pieces into one line of text. '''
	import itertools
	
	table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="1">'
	content = ''.join(list(itertools.chain(*content_tmp)))

	if layer:
		switch = {'components': '<TR><TD>Name</TD><TD colspan="2">Volume</TD><TD colspan="2">Conc</TD></TR>',
			  'thermocycle': '<TR><TD>Phase</TD><TD>Subpahse</TD><TD colspan="2">temp</TD><TD colspan="2">time</TD><TD colspan="2">cycles</TD></TR>'}
		header = switch[layer]		  	
		merge = '<' + table + header + content + '</TABLE>>'

	else:
		merge = '<' + table + content + '</TABLE>>'

	return merge


def add_thermo(job_A, job_B=None, changed=None, subphases=None, **kwargs):
	
	import itertools
	
	stack = []
	it = itertools.izip(job_A['phases'], job_B['phases'])
	
	while True:
		try:
			i,j = it.next()
			subphase_name = i.keys()[0]
			temp_A = i[i.keys()[0]]['temp']
			time_A = i[i.keys()[0]]['time']
			temp_B = j[j.keys()[0]]['temp']
			time_B = j[j.keys()[0]]['time']
			if subphases and subphase_name in subphases:
				if 'temp' in subphases[subphase_name] and 'time' not in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A) 	
		
				if 'time' in subphases[subphase_name] and 'temp' not in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A, time_B) 	
					
				if 'temp' in subphases[subphase_name] and time in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD>%s</TD><TD color="#015666"><font color="#015666">%s</font></TD><TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A, time_B) 			
					
			else:
				row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A) 			
				
			stack.append(row)
			
		# Change the last row or every phase to add in a cycles column:	
		except StopIteration:
			last_row = stack[-1]
			stack.pop(-1)
			if job_A['cycles'] == job_B['cycles']: 
				cycles = '</TD><TD>%s cycles</TD></TR>' %job_A['cycles'] 
				fixed_last_row  = last_row.replace('</TD></TR>',cycles)
				
			else:
				cycles = '</TD><TD>%s cycles</TD><TD>%s cycles</TD></TR>' %(job_A['cycles'], job_B['cycles'])
			
			fixed_last_row =last_row.replace('</TD></TR>',cycles)
			stack.append(fixed_last_row)	
			break
	return stack


def add_step_label(step, step_layer = False): 
	import textwrap
	wrapped = textwrap.wrap(step, 60)
	stack = []
	for w in wrapped:
		stack.append('<font>%s</font><br/>'%w)
	
	merge = '<' + ''.join(stack) +'>'	
	
	return merge

def set_title_label(title):

	stack = []
	name = '<TR><TD colspan="2">%s</TD></TR>'%(title.name)
	owner = '<TR><TD>Author: %s</TD><TD>Organization: %s</TD></TR>'%('None', str(title.owner))
	inheritance = '<TR><TD>Parent: %s</TD><TD>Children: %s</TD></TR>'%(str(title.parent), 'None')
	links = '<TR><TD>link to author: %s</TD><TD>Pubmed: %s</TD></TR>'%('Link Here', str(title.data['Reference_PMID'])) # str(title.data['Reference_URL'])
	timing = '<TR><TD>Date Created: %s</TD><TD>Duration: %s</TD></TR>'%(str(title.created), str(title.duration_in_seconds))
	stack = [name, inheritance, links, timing]
	return stack	

# <TD>%s</TD><TD color="#B82F3"><font color="#B82F3">%s</font></TD><TD color="#015666"><font color="#015666">%s</font></TD><TD colspan="2">%s</TD></TR>'%(self.name, )








