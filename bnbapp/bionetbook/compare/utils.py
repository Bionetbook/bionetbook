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
			content_tmp.append('<TR><TD><font color="#B82F3">%s</font></TD><TD><font color="#015666">%s</font></TD></TR>'%(x[i], y[i]))

		for j in unchanged:
			content_tmp.append('<TR><TD colspan="2">%s</TD></TR>'%(x[j]))	

		content = ''.join(content_tmp)
		merge = '<' + table + content + '</TABLE>>'	

		return merge


	if 'components' in kwargs: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
		''' assuming that the objectids of the reagents are the same'''
		# print 'conponents on'
		# count how many changes each reagent has, if 2 reagent names are different, write them last 

		if 'conc' in changed:
			_conc = '<TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>'%(str(x['conc'][0]),str(x['conc'][1]), str(y['conc'][0]),str(y['conc'][1]))
		if 'conc' in unchanged:
			_conc = '<TD colspan="2">%s</TD><TD colspan="2">%s</TD>'%(str(x['conc'][0]), str(x['conc'][1]))
		else:
			_conc = ''

		if 'vol' in changed:
			_vol = '<TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>'%(str(x['vol'][0]),str(x['vol'][1]), str(y['vol'][0]),str(y['vol'][1]))
		if 'vol' in unchanged:
			_vol = '<TD colspan="2">%s</TD><TD colspan="2">%s</TD>'%(str(x['vol'][0]), str(x['vol'][1]))
		
		else:
			_vol = ''


		if 'mass' in changed:
			_mass = '<TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD>'%(str(x['mass'][0]),str(x['mass'][1]), str(y['mass'][0]),str(y['mass'][1]))
		if 'mass' in unchanged:
			_mass = '<TD colspan="2">%s</TD><TD colspan="2">%s</TD>'%(str(x['mass'][0]), str(x['mass'][1]))
		
		else:
			_mass = ''

	return  _conc + _vol + _mass + '</TR>'

def add_html_cell(m):
	return '<TD>%s</TD>' %(m)

def merge_table_pieces(content_tmp):
	
	table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">'
	content = ''.join(content_tmp)
	merge = '<' + table + content + '</TABLE>>'
	return merge


# same = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>'% (kwargs['name'], x[])
# only_one = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>'%(kwargs['name'], x[])
# both = '<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR><TD>%s</TD><TD>%s</TD>' %