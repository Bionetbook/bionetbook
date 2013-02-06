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

def add_thermo(job_A, job_B=None, changed=None, unchanged=None, **kwargs):
	import itertools
	
	if 'subphases' in kwargs:
		subphases = kwargs['subphases']
	stack = []
	# if job_B:
	
	
	# else:
	# 	it = itertools.chain(job_A['phases'])
	if changed:
		# print 'changed: %s' % (changed)		
		# print 'subphases: %s'% (subphases)
		it = itertools.izip(job_A['phases'], job_B['phases'])
		for i,j in it:
			subphase_name = i.keys()[0]
			temp_A = i[i.keys()[0]]['temp']
			time_A = i[i.keys()[0]]['time']
			temp_B = j[j.keys()[0]]['temp']
			time_B = j[j.keys()[0]]['time']
			if subphase_name in subphases:
				if 'temp' in subphases[subphase_name] and 'time' not in subphases[subphase_name]:
					
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A) 	
					print 'temp: %s'% row
				if 'time' in subphases[subphase_name] and 'temp' not in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A, time_B) 	
					print 'time: %s'% row
				if 'temp' in subphases[subphase_name] and time in subphases[subphase_name]:
					row  = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, temp_B, time_A, time_B) 			
					print 'both:%s'% row 
			else:
				row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A) 			
				# print 'no suphase_name'
			stack.append(row)	
		print 'this is a stack for diff %s'%stack
	
	else:
		it = itertools.izip(job_A['phases'], job_B['phases'])
		for i,j in it:
			try:
				# i=it.next()
				# print 'i,j:', i,j
				subphase_name = i.keys()[0]
				temp_A = i[i.keys()[0]]['temp']
				time_A = i[i.keys()[0]]['time']
				temp_B = j[j.keys()[0]]['temp']
				time_B = j[j.keys()[0]]['time']
				row  = '<TR><TD>%s</TD><TD>%s</TD><TD colspan="2">%s</TD><TD colspan="2">%s</TD></TR>'%(job_A['name'],subphase_name, temp_A, time_A) 			
				# print row		
				stack.append(row)
				# print 'stack:', stack
			except StopIteration:
				print 'appending cycle space'
				stack.pop(-1)
				# print 'i_keys:%s, i[temp]%s '%(i.keys()[0],i[i.keys()[0]]['temp'])
				row = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s cycles</TD></TR>'%(job_A['name'],i.keys()[0], i[i.keys()[0]]['temp'], i[i.keys()[0]]['time'], job_A['cycles']) 	
				stack.append(row)

	

	print 'stack from else: %s'% row	
	return stack
			
# def get_thermo_changes(job_A, job_B):







