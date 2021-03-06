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

''' 
this is a parser for CVS formatted protocols and returns them in nested dictionaries as json format as default
run with:



'''


print 'starting protocol'
filename = sys.argv[1]
if len(sys.argv) >2:
	output_format = '.' + sys.argv[2]
else:
	output_format = '.yaml'


f=csv.reader(open(filename,'rU'))
rows = []

for line in f:
	rows.append('| '.join(line).split('|'))

def labelRowType(rows, rownum, cellchars):
	if cellchars[0] >= 1 :
		return 'Step' 
	if cellchars[2] > 1 and cellchars[3] > 1:
		return 'action'
	if cellchars[2] == 1 and cellchars[3] > 1: # and cellchars[0] == 0:
		return 'new_attribute'
	if cellchars[2] == 1 and cellchars[3] == 1 and cellchars [1] == 1:
		return 'Field'



def add_attribute(rownum,Stepnum,actionnum):

	attribute = {}
	attributetype = rows[rownum][3].strip()

	if 'sample' in attributetype:
		colnum = 4
		cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
		# print cellchars
		if 1 in cellchars[colnum:]:
			endcolumn = 4 + cellchars[4:].index(1)
		else:
			endcolumn = len(cellchars)
		for i in range(colnum,endcolumn): # add all specified attributes to the dict
			if len(rows[rownum + 1][i].strip())>0:
				attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
		return attribute


	if 'what' in attributetype and 'component' not in attributetype:
		attribute['what'] = rows[rownum][4].strip().replace(' ', '_').lower()
		return attribute	
		
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
		for i in range(colnum, len(cellchars)): # add all specified attributes to the dict
			if len(rows[rownum + 1][i].strip())>0:
				attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
		return attribute
	
	if 'step - remark' in attributetype: # and 'remark' in attributetype:
		steps[Stepnum]['remark'] = rows[rownum][4].strip()
		# return 'no update'

	if 'machine' in attributetype:
		attribute['machine'] = rows[rownum][4].strip().lower()
		return attribute

	if 'tool' in attributetype:
		attribute['tool'] = rows[rownum][4].strip().lower()
		return attribute

	if 'where' in attributetype:
		attribute['where'] = rows[rownum][4].strip().lower()
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
			if len(rows[rownum + 1][i].strip())>0:
				attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
		return attribute

	if 'component' in attributetype: 
		# attribute['location'] = [rownum,Stepnum,actionnum]
		Protocol['components-location'].append([rownum,Stepnum,actionnum])

	if 'remark' in attributetype:
		attribute['remark'] = rows[rownum][4].strip().lower()
		return attribute

	# else:
	# 	colnum = 4
	# 	cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
	# 	if 1 in cellchars[colnum:]:
	# 		endcolumn = 4 + cellchars[4:].index(1)
	# 	else:
	# 		endcolumn = len(cellchars)
	# 	for i in range(colnum, len(cellchars)): # add all specified attributes to the dict
	# 		if len(rows[rownum + 1][i])>2:
	# 			attribute[rows[rownum][i].strip().replace(' ', '_').lower()] = rows[rownum + 1][i].strip()
	# 	return attribute	

def add_component_list(header_row):		
	
	attribute = {'components': []}
	rownum = header_row +1
	colnum = 4
	# define width of componenets list:
 	cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
	while len(rows[rownum][3]) <2:
		tmp = {}
		for i in range(colnum, len(cellchars)): 
			if len(rows[rownum][i].strip())>0:
				key = rows[header_row][i].strip().replace(' ', '_').lower()
				if 'reagent_name' in key:
					tmp['name'] = rows[rownum][i].strip()
				else:
					tmp[key] = rows[rownum][i].strip()

		attribute['components'].append(tmp)
		rownum +=1	
	
		# attribute['components']['name'] = attribute['components']['reagent_name']
		# del(attribute['components']['reagent_name'])	
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
	'components-location': [],
	'protocol-reagents': {}
	}

# Add buffers and recipes:
# find step start:
step_start = [r+1 for r in range(7,30) if 'Step' in rows[r][0]]

for rownum in range(9, step_start[0]-1):
	if len(rows[rownum][0]) > 2:
		attribute = add_component_list(rownum)
		# relation= (rows[rownum][1].split(','))
		# Protocol['components-location'].append([rows[rownum], relation[0], relation[1]])
		Protocol['protocol-reagents'][rows[rownum+1][2]]=attribute
		continue
		  
# Populate the Protocol Dict with actions verbs atts fields and values

current_row = step_start[0]

steps = []
Stepnum = -1

for rownum in range(current_row, len(rows)): # pute each rows data in plac
	cellchars = [len(rows[rownum][cell]) for cell in range(len(rows[rownum]))]
	rowtype = labelRowType(rows, current_row, cellchars)
	if rowtype == 'Step':
		steps.append({})
		Stepnum +=1
		actionnum = 0
		steps[Stepnum]['stepnum'] =  Stepnum
		# step[Stepnum] = {'container'} : rows[rownum][1]
		steps[Stepnum]['actions']=  [] 
		steps[Stepnum]['actions'].append({})
		steps[Stepnum]['actions'][actionnum]['verb'] = rows[rownum][2].strip().replace(' ', '_').lower()
		attribute = add_attribute(rownum,Stepnum,actionnum)
		if attribute:
			if 'no update' in attribute.keys():
				continue
			steps[Stepnum]['actions'][actionnum] = dict(steps[Stepnum]['actions'][actionnum].items() + attribute.items())
		continue
		print Stepnum

	if rowtype == 'action':
		actionnum += 1
		steps[Stepnum]['actions'].append({'verb':rows[rownum][2].strip().replace(' ', '_').lower()})
		attribute = add_attribute(rownum,Stepnum,actionnum)
		if attribute:
			steps[Stepnum]['actions'][actionnum] = dict(steps[Stepnum]['actions'][actionnum].items() + attribute.items())
		else:
			steps[Stepnum]['actions'][actionnum] = dict(steps[Stepnum]['actions'][actionnum].items() + {}.items())
		continue
		print actionnum

   	if rowtype == 'new_attribute':
   		# verified that this is not a new action and not a new step
   		attribute = add_attribute(rownum,Stepnum,actionnum)
   		# assign the step number and action number
   		if attribute:
   			steps[Stepnum]['actions'][actionnum] = dict(steps[Stepnum]['actions'][actionnum].items() + attribute.items())
   		else:
   			steps[Stepnum]['actions'][actionnum] = dict(steps[Stepnum]['actions'][actionnum].items() + {}.items())
    	continue


	if rowtype == 'reagent':
		attribute = add_component_list(row[rownum])
		relation= (rows[rownum][1].split(','))
		# Protocol['components-location'].append([rows[rownum], relation[0], relation[1]])
		Protocol['protocol-reagents'][rows[rownum+1][2]]=attribute
		continue



# Summarize all component lists into one variable:
Protocol['steps'] = steps
for j in Protocol['components-location']:
	attribute = add_component_list(j[0])
	if attribute:
   		steps[j[1]]['actions'][j[2]]['components'] = attribute.values()[0]
   	else:
   		steps[j[1]]['actions'][j[2]]['components'] = {}
	

# Write the output file in selected format:	
fname_pure= filename[filename.index('/')+1:filename.index('.')] + output_format

if output_format == '.yaml':
	fname = 'new_YAML_files/' + fname_pure 
	stream = file(fname, 'w')
	yaml.dump(Protocol, stream)

if output_format == '.json':
	fname = '/Users/Oren/Coding/bionetbook/bnbapp/new_JSON_files/' + fname_pure 
	stream = open(fname, 'w')
	stream.write(json.dumps(Protocol))
	stream.close()

print '%s'%(fname)