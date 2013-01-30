def set_html_label(x,y,changed, unchanged):

	''' label is an HTML object and for automation sake, created by concatenating a few peices:
				table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">' --> defines the table properties in HTML
				content = '<TR><TD>{0}</TD><TD>{1}</TD></TR><TR><TD colspan="2">{2}</TD></TR>' --> generates the content of the comparison table
				merge = '<' + table + content + '</TABLE>>'	--> merges the pieces into one line of text. '''

	table = '<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5">'
	content_tmp = []
	content = []
	

	
	# format the HTML component:
	content_tmp = []
	for i in changed:
		content_tmp.append('<TR><TD>%s</TD><TD>%s</TD></TR>'%(x[i], y[i]))

	for j in unchanged:
		content_tmp.append('<TR><TD colspan="2">%s</TD></TR>'%(x[j]))	

	content = ''.join(content_tmp)
	merge = '<' + table + content + '</TABLE>>'	

	return merge
