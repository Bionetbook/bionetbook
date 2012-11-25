# updateVerbAttrib
# Author Oren Schaedel
# Date: 9/12/2012
# Version: 1.0

# this script updates the attributes and data structures that each verb recieves. 
# The script makes 2 dictionaries, a verb-attribute and an attribute-datatype
# it calls the verbs from the verbs_attributes.txt file in the bionetbook/docs folder
# It calls the data types from attributes_datatype.txt
# The data on these files was manually imported from the google docs spreadsheet 'Attribtue Template' (spelling mistake intended)
# The script opens up each verb.py file, DELETES the old attributes and RE-WRITES the new ones. 


# Verb-attribure list is imported from here:
newFile = open('verb_attributes.txt','r')

# import file and put into a list
lines=[]
for line in newFile:
	lines.append(line)

tot = len(lines)

# create the verbs dict
verbs={}


for line in lines:
	tmp=line.strip('\n').split('\t')
	if tmp[0] not in verbs:
		verbs[tmp[0]]=[]
	verbs[tmp[0]].append(tmp[1]) 

newFile.close()
print len(verbs), len(verbs.values())

# import the attribute-data type list

datatypes = open('attribute_datatype.txt','r')
# don't use readlines(), it strips the '\t' and hurt sorting lines. 
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

		attributes[tmp[0]].append(tmp[1] + ' = ' + tmp[2])	
			
datatypes.close()
print len(attributes)

#Add the lines to each verb file


for verb in verbs:
	try:
		current_verb = '../bionetbook/verbs/forms/' + verb +'.py'
		current_verb_file = open(current_verb,'r')
		lines = current_verb_file.readlines() # read all lines to capture the top 9. 
		current_verb_file.close()
	except IOError:
		continue


	current_verb_file = open(current_verb,'w')
	current_verb_file.writelines(lines[0:8]) # write only the top 9 rows, all attributes will be deleted
	for atts in verbs[verb]: # run through all attributes
		if atts in attributes: # concurrence between verbs list and attributes list
			datatypes = attributes[atts] # list out all datatypes for each attribute
			for line in datatypes: # paste each attribute = datatype in a new row. 
				current_verb_file.write('\n    %s' % line) # the four spaces are necessary, not a tab. 

	current_verb_file.close()			
	







