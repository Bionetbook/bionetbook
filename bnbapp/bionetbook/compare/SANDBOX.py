	SANDBOX	

import itertools
class CopmareNodeBase(protocol_A, protocol_B, object_A, object_B, **kwargs):
    """ Version - 1 : inherit from the Base class of protocol components, machines and thermocycle 
    and return a Protocol object that has a new diff attribute with an pk-objectid reference. 
    this class will have a to_json, to_dot, to_svg, to_html etc methods that draw out the 
    CompareNodeBase in each of those callers formats. 


    Version 2:
    the diff works recursively throught the actions and finds all the diffs along the way. 
    a diff line is created 
     """

    # protocol_A and protocol_B are both ProtocolPlot objects>

    # if pk_A and pk_b are defined, then look in those protocols,
    # else, look in this protocol only. 
     
    # determine what type the object is (step, action, machine, thermo, component)
    
    
    layer_A = protocol_A.nodes[object_A].__class__
    layer_B = protocol_B.nodes[object_B].__class__
    if layer_A != layer_B:
        return 'these objects are from different layers and cannot be compared'

    parent_layer = layer_A.parent.__class__

    rank_list = [] # this is the list fo ranked objects
    actions_A = protocol_A.get_actions
    actions_B = protocol_B.get_actions
    # determine that there are no verbs out of order:
    

    it = itertools.izip(verbs_A, verbs_B)
    for i,j in it:

        D = DDiffer( object_A, object_B )

    line = []

    if len(D.changed) > 0 :
        line = ()
        DDiffer(object_A, object_B, rank_list) 

    else: 
        line = [
        ( protocol_A.nodes[object_A].pk, protocol_A.nodes[object_A]['name'] ),
        ( protocol_B.nodes[object_B].pk, protocol_B.nodes[object_B]['name'] )
        ]

        rank_list.append(line)

        

   


    







class DDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """


    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
        self.querry = (self.current_dict, self.past_dict)
        # self.added = self.new
        # self.removed = self.deleted
        # self.changed = self.modified
        # self.unchanged = self.same
        # self.layer = 0
    
    @property
    def A_added(self):
        return list(self.set_current - self.intersect)
    
    @property
    def B_added(self):
        return list(self.set_past - self.intersect)
    
    @property   
    def changed(self, name = False, objectid = False, slug = False):
        delta = list(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
        if name:
            delta.pop(delta.index('name'))
        if objectid:
            delta.pop(delta.index('objectid'))
        if slug:
            delta.pop(delta.index('slug'))
        return delta
    
    @property
    def same(self):
        return list(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

    @property
    def inheritance(self):
        if self.changed > 0:
            if type(self.changed) in not str:



    



def compare_two_ordered_lists(lst1, lst2):

    if len(lst1) > len(lst2):
        longer = lst1
        shorter = lst2
    else:
        longer = lst2 
        shorter = lst1 


    start = 0
    try:
        for item in shorter:
            start = longer.index(item, start) + 1
    except ValueError:
        return False
    return True     


def align_two_lists(ls1, ls2):
    ''' aligns the objectids between two lists:
    Checks that both list objects are in the same order
    Aligns the objectids, padds None if there are no matches'''

    ordered = compare_two_ordered_lists(ls1, ls2)

    if not ordered:
        print 'do something with lists that arent ordered properly.'

    alignment = []
    
    # Find the objects that are not aligned:
    no_partner = set(ls1).symmetric_difference(set(ls2))

    partners = set(ls1).intersection(set(ls2))  

    combined_list = set(ls1).union(set(ls2))

    # add the verbs that are in both lists:

    for i in combined:
        if i in partners:
            # add it to the alignment
            alignment.append((i,i))
        else:
            if i in ls1 and i not in ls2:
                alignment.append((i, None))   
            else:
                alignment.append((None, i))

    # trial 2:
    
    F = itertools.izip_longest(ls1, ls2)

    F = list(F) 

    for i,j in F:
        if i == j:
            alignment.append((i,j))
        else:
             # both objects are in the lists and not aligned:
             if i in ls2 and j not in ls1:
                alignment.append((None,j))
             if i in ls2 and j not in ls1:   

    



                   

    


                    # We have a list of edges with a difference score
# figure out which nodes are real edges
# remove canditates from a:b mapping:


reff = matches[0][0]
cand = matches[0][1]
score = matches[0][2]
out2 = []

for i in matches:
	if i[0] != reff: 
		out2.append([reff, cand, score])		
		reff = i[0]
		score = i[2]
		cand = i[1]

	else:
		if i[2] < score:
			score = i[2]
			cand = i[1]	

	if i[0] == matches[-1][0]:
		# out2.append([reff, cand, score])
		continue
				
			

for i in matches:
	
	if i[0] != reff: 
		reff = i[0]
		score = i[2]
		cand = i[1]
		tmp = ([reff, cand, score])		 

	else:
		if i[2] < score:
			score = i[2]
			cand = i[1]	


# Find the rows where matching 1 neighbor isnt enough:

# find the edges that need to be ranked:
a_s = [r[0] for r in comparators]
b_s = [r[1] for r in comparators]

a_uniques = [ x for x in a_s if a_s.count(x) == 1]
a_diffs = [ x for x in a_s if a_s.count(x) > 1]

b_uniques = [ x for x in b_s if b_s.count(x) == 1]
b_diffs = [ x for x in b_s if b_s.count(x) > 1]

a_uniq_in_comparator = [a_s.index(r) for r in a_uniques]
b_uniq_in_comparator = [b_s.index(r) for r in b_uniques]

if len(set(a_uniq_in_comparator)-set(b_uniq_in_comparator)):
	diffs = list(set(range(len(comparators)))- set(a_uniq_in_comparator))
	diff = [comparators[r] for r in diffs]


[u'adrmwt', u'lk1yt0', 5],
[u'adrmwt', u'i7w4wg', 5],
# 1 [u'adrmwt', u'8v7w7q', 0],

[u'bavsb0', u'lk1yt0', 4],
[u'bavsb0', u'i7w4wg', 0],
# 2 [u'bavsb0', u'8v7w7q', 5],

[u'kbzqcb', u'd6m0hh', 0],
[u'kbzqcb', u'nwv41j', 0],

[u'thfavi', u'd6m0hh', 0],
[u'thfavi', u'nwv41j', 0]



# Trail 3: 
# working: gap = 1,2  
# not working: order switch, more than 2 lists, if there are some gaps and then an index rematch (first[i] == second[i]) are not being re aligned properly 

def align_lists ( actions_A, actions_B):
    import itertools
    first = list(actions_A)
    second = list(actions_B)     
    len_1 = len(actions_A)
    len_2 = len(actions_B)
    if len_1 > len_2:
        longer = len_1
    else:
        longer = len_2

    for i in range(longer):
        if first[i] == second[i]:
            # check that there current sequnce aligns:
            continue
        else:
            # ls2 has an extra action
            if first[i] in actions_B and second[i] not in actions_A:
                first.insert(i, None) 
            if second[i] in actions_A and first[i] not in actions_B:
                second.insert(i, None) 
            if first[i] in actions_A and first[i] in actions_B:
                idx_a = 
                idx_b = second.index(first[i])
                while idx_b >     



    F  = itertools.izip_longest(first,second)
    for i, j in F:
        print i,j  

    return itertools.izip_longest(first,second)             


        # if first[i] not in ls2:
        #     second.insert(i,None)
def align_lists ( actions_A, actions_B):
    import itertools

    first = list(actions_A)
    second = list(actions_B)     
    len_1 = len(actions_A)
    len_2 = len(actions_B)
    input_cnt_a = 0
    output_cnt_a = 0
    input_cnt_b = 0
    output_cnt_b = 0
    if len_1 > len_2:
        longer = len_1
    else:
        longer = len_2

    output = {}

    for i in range(longer):
        if first[i] == second[i]:
            # check that there current sequnce aligns:
            result.append((first[output_cnt_a], second[output_cnt_b]))
            # output_cnt_a +=1
            # output_cnt_b +=1
        else:
            # ls2 has an extra action
            if first[i] in actions_B and second[i] not in actions_A:
                output.append((i, None) 
            if second[i] in actions_A and first[i] not in actions_B:
                output.append((i, None) 
            if first[i] in actions_A and first[i] in actions_B:
                idx_a = first.index(i)
                idx_b = second.index(first[i])
                if idx_b > idx_a:
                    output.append((None, i) 



    # F  = itertools.izip_longest(first,second)
    # for i, j in F:
    #     print i,j          
    
    return output





