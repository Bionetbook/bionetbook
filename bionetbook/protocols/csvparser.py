# heuristic for parsing the csv files

# this is a loop running through all rows and assigning the meta data cells in place it should stop at rows[10][0]  'Step number'
# itterator layout:
# Steps: [{},{},{}]; each list item is a dict. 
#		 - itterator = Stepnum 
# Stepnum.dict: {'actions':  = [{},{},{}],
#			  'container'} = raw_text,
#			  'reamrks' = raw_text}
#		 - itterator = .keys()   
# actions: [{},{},{}]; each list item is a dict.   
# 			- itterator = actionnum
# actionnum.dict: {'verb':[rownum][cellnum],
#				   attribute_name['itterator'] = conditional_statement
#			- itterator = rows[rownum][4] = attributetype	
import sys
import csv
import yaml
import json

filename = 'dna_extract_bones.csv'
f=csv.reader(open(filename,'rU'))
rows = []

for line in f:
	rows.append('| '.join(line).split('|'))

def labelRowType(cellchars):
	if cellchars[0] == 1:
		return 'Step'
	if cellchars[2] > 1 and cellchars[3] > 1:
		return 'Action'
	if cellchars[2] == 1 and cellchars[3] > 1: # and cellchars[0] == 0:
		return 'new_attribute'
	if cellchars[2] == 1 and cellchars[3] == 1 and cellchars [1] == 1:
		return 'Field'


def add_attribute(rownum,Stepnum,actionnum):

	attribute = {}
	attributetype = rows[rownum][3].strip()
	if 'what' in attributetype and 'component' not in attributetype:
		attribute['what'] = rows[rownum][4].strip().replace(' ', '_').lower()
		return attribute	
		
	# if 'what' in attributetype and 'components'  in attributetype:
	# 	attribute['what - component'] = 'later'
	# 	return attribute

	if  'protocol' in attributetype and 'component' not in attributetype:
		attribute[rows[rownum][3].strip().replace(' - ', '_').lower()] = rows[rownum][4]
		return attribute

	if 'why' in attributetype:
		attribute['why'] = rows[rownum][4].strip().lower()
		return attribute
		
	if 'how' in attributetype and '-' not in attributetype:
		attribute['how'] = rows[rownum][4].strip().lower()	
		return attribute

	if len(attributetype) ==1:
		attribute['null'] = 'empty'
		return attribute

	if 'duration' in attributetype:
		colnum = 4
		cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
		if 1 in cellchars[colnum:]:
			endcolumn = 4 + cellchars[4:].index(1)
		else:
			endcolumn = len(cellchars)
		for i in range(colnum, endcolumn): # add all specified attributes to the dict
			if len(rows[rownum + 1][i])>2:
				attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
		return attribute
	
	if 'step' in attributetype: # and 'remark' in attributetype:
		steps[Stepnum]['remark'] = rows[rownum][4].strip()
		# return 'no update'
		
	if 'machine' in attributetype:
		attribute['machine'] = rows[rownum][4].strip().lower()
		return attribute	

	if '-' in attributetype and 'component' not in attributetype and 'protocol' not in attributetype and 'step' not in attributetype:
		# catch all 'question' - 'parameter' such as Min time = '2'
		colnum = 4
		cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
		# print cellchars
		if 1 in cellchars[colnum:]:
			endcolumn = 4 + cellchars[4:].index(1)
		else:
			endcolumn = len(cellchars)
		for i in range(colnum,endcolumn): # add all specified attributes to the dict
			if len(rows[rownum + 1][i])>2:
				attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
		return attribute

	if 'component' in attributetype: 
		# attribute['location'] = [rownum,Stepnum,actionnum]
		Protocol['components-location'].append([rownum,Stepnum,actionnum])

	if 'remark' in attributetype:
		attribute['remark'] = rows[rownum][4].strip().lower()
		return attribute

	if 'remark' in attributetype:
		attribute['remark'] = rows[rownum][4].strip().lower()
		return attribute	

def add_component_list(header_row):		
	
	attribute = {'component - list': []}
	rownum = header_row +1
	colnum = 4
	# define width of componenets list:
 	cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
	while len(rows[rownum][3]) <2:
		tmp = {}
		for i in range(colnum, len(cellchars)): 
			if len(rows[rownum][i])>2:
				tmp[rows[header_row][i].strip().replace(' ', '_').lower()] = rows[rownum][i].strip()
		attribute['component - list'].append(tmp)
		rownum +=1	
	return attribute




#initiate protocol with meta data
Protocol =  {
	'Name': rows[0][1].strip(),
	'Input': rows[1][1].strip(),
	'Output': rows[2][1].strip(),
	'Remarks': rows[3][1].strip(),
	'Reference_PMID': rows[4][1].strip(),
	'Reference_URL': rows[5][1].strip(),
	'Reference_DOI': rows[6][1].strip(),
	'Category_tags': rows[7][1].strip(),
	'Specific_tags': rows[8][1].strip(),
	'components-location': []
	}
# Populate the Protocol Dict with actions verbs atts fields and values
current_row = 11
steps = []
Stepnum = -1

for rownum in range(current_row, len(rows)): # pute each rows data in plac
	cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
	rowtype = labelRowType(cellchars)
	if rowtype == 'Step':
		steps.append({})
		Stepnum +=1
		actionnum = 0
		steps[Stepnum]['stepnum'] =  Stepnum
		# step[Stepnum] = {'container'} : rows[rownum][1]
		steps[Stepnum]['Actions']=  [] 
		steps[Stepnum]['Actions'].append({})
		steps[Stepnum]['Actions'][actionnum]['verb'] = rows[rownum][2].strip().replace(' ', '_').lower()
		attribute = add_attribute(rownum,Stepnum,actionnum)
		if attribute:
			if 'no update' in attribute.keys():
				continue
			steps[Stepnum]['Actions'][actionnum] = dict(steps[Stepnum]['Actions'][actionnum].items() + attribute.items())
		continue

	if rowtype == 'Action':
		actionnum += 1
		steps[Stepnum]['Actions'].append({'verb':rows[rownum][2].strip().replace(' ', '_').lower()})
		attribute = add_attribute(rownum,Stepnum,actionnum)
		if attribute:
			steps[Stepnum]['Actions'][actionnum] = dict(steps[Stepnum]['Actions'][actionnum].items() + attribute.items())
		else:
			steps[Stepnum]['Actions'][actionnum] = dict(steps[Stepnum]['Actions'][actionnum].items() + {}.items())
		continue

   	if rowtype == 'new_attribute':
   		# verified that this is not a new action and not a new step
   		attribute = add_attribute(rownum,Stepnum,actionnum)
   		# assign the step number and action number
   		if attribute:
   # 			if 'str' in str(type(attribute)):
			# 	continue
			# else:
   			steps[Stepnum]['Actions'][actionnum] = dict(steps[Stepnum]['Actions'][actionnum].items() + attribute.items())
   		else:
   			steps[Stepnum]['Actions'][actionnum] = dict(steps[Stepnum]['Actions'][actionnum].items() + {}.items())
    	continue

   	# else:
   	# 	continue

Protocol['steps'] = steps
for j in Protocol['components-location']:
	attribute = add_component_list(j[0])
	if attribute:
   # 			if 'str' in str(type(attribute)):
			# 	continue
			# else:
   		steps[j[1]]['Actions'][j[2]] = dict(steps[j[1]]['Actions'][j[2]].items() + attribute.items())
   	else:
   		steps[j[1]]['Actions'][j[2]] = dict(steps[j[1]]['Actions'][j[2]].items() + {}.items())
	# steps[j[1]]['Actions'][j[2]] = 
	# Protocol['steps'] = add_component_list(Protocol['steps'])		



fname_new= filename[:filename.index('.')] + '.yaml'
stream = file(fname_new, 'w')
yaml.dump(Protocol, stream)





	    # add this later, figure out how to send a vaiable that will change the level
	    # if attributetype = 'step - remark':
	    # 	step[Stepnum]['remarks'] = rows[rownum[4]]
	    # 	continue



