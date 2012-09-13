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








