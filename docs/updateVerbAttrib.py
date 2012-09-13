# updateVerbAttrib


# this script updates the attributes and data structures that each verb recieves. 

# Verb-attribure list is imported from here:
newFile = open('/Users/Oren/Dropbox/BNB_Software_Development/Curation/Parsing/verb_att_list_all_protocols.txt','r')

# import file and put into a list
lines=[]
for line in newFile:
	lines.append(line)

tot = len(lines)

# create the verbs dict
verbs={}

# populate the verbs dict with 
for i in range(tot):
	if lines[i][0]!='\t':
		tmp = lines[i].strip('\n').split('\t')
		if tmp[0] not in verbs: 
			verbs[tmp[0]]=[]

		if tmp[1] not in verbs[tmp[0]]:
			verbs[tmp[0]].append(tmp[1])
			verb = tmp[0]

	if lines[i][0]=='\t' and lines[i][1]!='\n': 
		tmp = lines[i].strip('\n').split('\t')
		if tmp[1] not in verbs[verb]:
			verbs[verb].append(tmp[1])


newfile.close()

# import the attribute-data type list

datatypes = open('/Users/Oren/Coding/bionetbook/docs/attribute_datatype.txt','r')

rows = []
for line in datatypes:
	rows.append(line)

tot = len(rows)

attributes={}
for i in range(tot):
	if rows[i][0]!='\t': 
		tmp = rows[i].strip('\n').split('\t')
		# check for new attribute
		if tmp[0] not in attributes: 
			attributes[tmp[0]]=[]

		attributes[tmp[0]].append(tmp[1] + '=' + tmp[2])	
			
datatypes.close()

# Add the lines to each verb file

for verb in verbs:
	try:
		current_verb = '/Users/Oren/Coding/bionetbook/bionetbook/verbs/forms/' + 'test' +'.py'
					
	except IOError
		continue
		
	current_verb_file = open(current_verb,'wa')

	for atts in verbs[verb]:
		if atts in attributes:
			datatypes = attributes[atts]
			for line in tmp:
				current_verb_file.write('\n%s' % tmp[datatypes])


	







