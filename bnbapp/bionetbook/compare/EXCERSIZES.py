def flatten_list(a, result=None):
    """Flattens a nested list.

        >>> flatten_list([ [1, 2, [3, 4] ], [5, 6], 7])
        [1, 2, 3, 4, 5, 6, 7]
    """
    if result is None:
        result = []

    for x in a:
        if isinstance(x, list):
            flatten_list(x, result)
        else:
            result.append(x)

    return result

    o =[ [1, 2, [3, 4] ], [5, 6], 7, [1, 2, 3, 4, 5, 6, 7] ] 



def exp(x, n):
    
    if n == 0:
        return 1
    else:
        return x * exp(x, n-1)





def flatten_dict(a, result = None):
	''' flattens a nested dict:
	{'a': 1, 'b': {'x': 2, 'y': 3}, 'c': 4} -- >
	{'a': 1, 'b.x': 2, 'b.y': 3, 'c': 4}
	'''

	if result is None:
		result = {}
	
	for k,v in a.items(): 
		if isinstance(v, dict):
			for child, values in v.items():
				new_keys['%s.%s'%(k,child)] = values 
				flatten_dict(new_keys, result)


		else:
			result[k] = v

	return result		


Dict = {'a': 1, 'b': {'x': 2, 'y': 3}, 'c': {'g':4,'r':{'t':45,'y': {'r':23},'D':34}}}    



