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
    ''' flattens a nested dict:{'a': 1, 'b': {'x': 2, 'y': 3}, 'c': 4} -- >{'a': 1, 'b.x': 2, 'b.y': 3, 'c': 4}'''
    if result is None:
        result = {}

    for k,v in a.items(): 
        if isinstance(v, dict):
            for child, values in v.items():
                new_keys['%s.%s'%(k,child)] = values 
                flatten_dict(new_keys, result)
                print child, values
        else:
            result[k] = v

    return result		


Dict = {'a': 1, 'b': {'x': 2, 'y': 3}, 'c': {'g':4,'r':{'t':45,'y': {'r':23},'D':34}}}    





first = json.loads('{"first_name": "Poligraph", "last_name": "Sharikov"}')
second = json.loads('{"first_name": "Poligraphovich", "pet_name": "Sharik"}')

df = Diff(first, second)

df.difference is ["path: last_name"]

Diff(first, second, vice_versa=True) gives you difference from both objects in the one result.

df.difference is ["path: last_name", "path: pet_name"]

Diff(first, second, with_values=True) gives you difference of the values strings.





