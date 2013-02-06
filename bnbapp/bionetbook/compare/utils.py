def set_html_label(x,y,changed, unchanged, **kwargs):

	''' label is an HTML object and for automation sake, created by concatenating a few peices:
				table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">' --> defines the table properties in HTML
				content = '<TR><TD>{0}</TD><TD>{1}</TD></TR><TR><TD colspan="2">{2}</TD></TR>' --> generates the content of the comparison table
				merge = '<' + table + content + '</TABLE>>'	--> merges the pieces into one line of text. '''

	table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">'
	content_tmp = []
	content = []
	content_tmp = []


	if 'machine' in kwargs:

	# format the HTML component:
		for i in changed:
			content_tmp.append('<TR><TD color="#C0C0C0"><font color="#B82F3">%s</font></TD><TD color="#C0C0C0"><font color="#015666">%s</font></TD></TR>'%(x[i], y[i]))

		for j in unchanged:
			content_tmp.append('<TR><TD color="#C0C0C0" colspan="2">%s</TD></TR>'%(x[j]))	

		content = ''.join(content_tmp)
		merge = '<' + table + content + '</TABLE>>'	

		return merge


	if 'components' in kwargs: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
		''' assuming that the objectids of the reagents are the same'''

		# count how many changes each reagent has, if 2 reagent names are different, write them last 
		
		_conc = ''
		_vol = ''
		_mass = ''

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


		if 'mass' in changed and 'mass' not in changed:
			_mass = '<TD color="#B82F3"><font color="#B82F3">%s</font>%</TD><TD color="#015666"><font color="#015666">%s</font></TD>'%(str(x['mass'][0]) + str(x['mass'][1]), str(y['mass'][0]) + str(y['mass'][1])) # <TD>%s</TD><TD>%s</TD>
		if 'mass' in unchanged and 'mass' not in unchanged:
			_mass = '<TD color="#C0C0C0" colspan="2">%s</TD>'%(str(x['mass'][0]) + str(x['mass'][1])) # <TD colspan="2">%s</TD>

		return  _conc + _vol + _mass + '</TR>'


def add_html_cell(m):
	return '<TD>%s</TD>' %(m)

def merge_table_pieces(content_tmp):
	import itertools

	table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">'
	content = ''.join(list(itertools.chain(*content_tmp)))
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
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A) 	
		
				if 'time' in subphases[subphase_name] and 'temp' not in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A, time_B) 	
					
				if 'temp' in subphases[subphase_name] and time in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A, time_B) 			
					
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
			print 'after adding last row: %s' %stack
			break
	return stack









