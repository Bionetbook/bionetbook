def map_def_order(filename):
	''' add filename in absolute path'''

	r = open(filename, 'r')

	lines = []

	for line in r:
		lines.append(line)

	r.close()
	
	# find defs:

defs = []
selfs = []
cnt = 0
for line in lines:
	if 'def' in line:
		defs.append((line,cnt))	
	if 'self' in line:
		selfs.append((line,cnt))	
	cnt+=1	

	defs_clean = []

	for line in defs:
		if ":" in line[0] and '#' not in line[0] and '__' not in line[0]:
			defs_clean.append(line)

	f_names = []

	for line in defs_clean:
		start = line[0].index('def') + 4
		finish = line[0].index('(')
		f_names.append((line[0][start:finish], line[1]))

	dependencies = {}	
	
	for func in f_names:
		if 


