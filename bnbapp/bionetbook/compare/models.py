from django.db import models

import pygraphviz as pgv 
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel
from compare.utils import html_label_one_protocol, html_label_two_protocols, add_html_cell, merge_table_pieces, add_thermo, set_title_label, add_step_label 

class DictDiffer(object):
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
    def added(self):
        return list(self.set_current - self.intersect)
    def removed(self):
        return list(self.set_past - self.intersect)
    def changed(self, **kwargs):
        delta = list(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
        if 'name' in delta and 'name' in kwargs:
            delta.pop(delta.index('name'))
        if 'objectid' in delta and 'objectid' in kwargs:
            delta.pop(delta.index('objectid'))
        if 'slug' in delta and 'slug' in kwargs:
            delta.pop(delta.index('slug'))
        return delta
    def unchanged(self):
        return list(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


class ProtocolPlot(Protocol):

    class Meta: 
        proxy = True

    def __init__(self, *args, **kwargs):
        super(ProtocolPlot, self).__init__(*args, **kwargs)
    
        self.agraph = pgv.AGraph(ranksep = '0.2')  

        self.pks = [self.nodes[r].pk for r in self.get_actions] # list of actions in pk-objectid format
    def plot(self, **kwargs):
        # super(ProtocolPlot, self).__init__(**kwargs)
        # self.prot = Protocol.objects.get(name__icontains=protocol_name)
        
        for i in range(1, len(self.pks)):
            self.agraph.add_edge(self.pks[i-1],self.pks[i])
            e = self.agraph.get_edge(self.pks[i-1], self.pks[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = '#B82F3' 
            n=self.agraph.get_node(self.pks[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = '10'
            n.attr['style'] = 'rounded'
            n.attr['height'] = '0.2'
            n.attr['label']= self.nodes[self.get_actions[i]]['verb']

        n = self.agraph.get_node(self.pks[0])
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = 'rounded'
        n.attr['height'] = '0.2'
        n.attr['label']=self.nodes[self.get_actions[0]]['verb']
        
        
    def add_layer(self, **kwargs):
        print kwargs['layers']
        if 'machine' in kwargs['layers']:
            machines_layer = True
        else:
            machines_layer = False 
        
        if 'component' in kwargs['layers']:
            components_layer = True
        else:
            components_layer = False 
        
        if 'thermo' in kwargs['layers']:
            thermocycle_layer = True
        else:
            thermocycle_layer = False

        for verb in self.get_actions:
            if 'machine' in self.nodes[verb].keys():  # object has only one child:
                x = self.nodes[verb]['machine'].summary
                content = html_label_one_protocol(x, machine = True) 

                # --->  create a compare-graph-object that will apear between the 2 base diagrams:
                if machines_layer:
                    print 'adding machine layer'
                    diff_object = self.nodes[verb]['machine'].pk
                    ea = self.agraph.add_edge(self.nodes[verb].pk,diff_object)
                    # eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)

                # set all diff objects on same rank:
                    N = self.agraph.add_subgraph([self.nodes[verb].pk, diff_object], rank = 'same')#, rankdir='LR') #, name='%s'%(layer_names[nc])) 
                
                # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'plaintext'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['fontsize'] = '10'
                    # set label:
                    s.attr['label'] = merge_table_pieces(content)
                
                # <---
            if 'components' in self.nodes[verb].keys(): 


                if len(self.nodes[verb]['components']) ==0:
                    continue

                else:
                    components_a = [r['objectid'] for r in self.nodes[verb].children]
                    scores = [] # tracks the error rate of a matching components
                    content = [] # gets the html strings
                    for m in components_a: 
                        tmp = html_label_one_protocol(self.nodes[m].summary, components = True) 
                        content.append(tmp)
                            
                    if components_layer:
                        print 'adding components layer'
                        diff_object = self.nodes[components_a[0]].pk 
                        ea = self.agraph.add_edge(self.nodes[verb].pk,diff_object)
                        N = self.agraph.add_subgraph([self.nodes[verb].pk, diff_object], rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc])) 
                        
                        # set layout and colors
                        s = self.agraph.get_node(diff_object)
                        s.attr['shape'] = 'plaintext'
                        s.attr['color'] = '#C0C0C0'
                        s.attr['style'] = 'rounded'
                        s.attr['fontsize'] = '8'
                        s.attr['label'] = merge_table_pieces(content, 'components')

            # if 'thermocycle' in self.nodes[verb].keys():
            #     import itertools
            #     # get all thermo children:
            #     phases = [r['objectid'] for r in self.nodes[verb_a].children]
            #     # phases_B = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                
            #     table = []
            #     for thermo in phases:
            #         job = self.nodes[thermo].summary
            #         # job_B = self.protocol_B.nodes[thermo].summary
            #         # print 'thermo is %s, \n A: %s + \n, B: %s'%(thermo, job_A['name'], job_B['name'])
            #         # d = DictDiffer(job_A, job_B)
            #         # if 'phases' in d.changed() or 'cycles' in d.changed():
            #             # go through all items in both phases
            #         # it = itertools.izip(job_A['phases'], job_B['phases']) 
                    
            #         for i in phases: # getting the subphase name that is different
            #             subphase_A = i
                        
            #             # f = DictDiffer(subphase_A, subphase_B)
            #             if f.changed():
            #                 L = f.changed() 
                            
            #                 subphases = {}
            #                 for each_subphase in L:
            #                     # subphases[each_subphase] = [] 
            #                     g = DictDiffer(subphase_A[each_subphase], subphase_B[each_subphase])    
            #                     subphases[each_subphase] = g.changed()
                                
                    
            #         tmp = add_thermo(job_A, job_B, d.changed(), subphases)
            #         table.append(tmp)
            #         continue
        
            #         if 'name' in d.changed():
            #             print 'name changed'    

            #         else:
            #             tmp = add_thermo(job_A, job_B)
            #             table.append(tmp)
                            
            #     diff_object = self.protocol_A.nodes[phases[0]].pk 
            #     ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
            #     eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)     
            #     N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', name = self.protocol_A.nodes[verb_a].pk) #, name='%s'%(layer_names[nc])) 
                
            #     # set layout and colors
            #     s = self.agraph.get_node(diff_object)
            #     s.attr['shape'] = 'box'
            #     s.attr['color'] = '#C0C0C0'
            #     s.attr['style'] = 'rounded'
            #     s.attr['label'] = merge_table_pieces(table, 'thermocycle')                

    def remove_layer(self): #, layer_names):
        self.agraph.remove_nodes_from([(v) for k,v in self.edges_list])
        # [self.agraph.remove_subgraph(name=r) for r in layer_names]


    def get_svg(self):
        self.agraph.layout('dot')
        return self.agraph

    def get_graph(self, agraph):
        agraph = self.agraph
        agraph.layout('dot')
        return agraph   

    def same_rank_objects_by_1st_degree_nbrs(self, protocol_B):


        # a = ProtocolPlot.objects.get(name__icontains=protocol_A)  
        b = ProtocolPlot.objects.get(name__icontains=protocol_B)
        
        a_actions = [r[2] for r in self.get_action_tree('objectid')]
        b_actions = [r[2] for r in b.get_action_tree('objectid')]

    
        comparator = []

        for idxa in a_actions:
            
            a_name = self.nodes[idxa]['verb']
            if 'machine' in self.nodes[idxa].keys():
                a_type = 'machine'
                a_child = self.nodes[idxa]['machine']['objectid']
            # if 'components' in self.nodes[idxa].keys():
            else: 
                if 'components' not in self.nodes[idxa] or len(self.nodes[idxa]['components']) == 0:
                    a_type = 'other'
                    a_child = None

                else: 
                    a_type = 'components'
                    a_child = [r['objectid'] for r in self.nodes[idxa]['components']]
            
            a_parent = self.nodes[idxa].parent['objectid'] # pointer to the step object
            idx_of_a = a_actions.index(idxa)
            
            if idx_of_a == 0: 
                a_previous = self.nodes[idxa]['objectid']
                a_nextt = self.nodes[a_actions[idx_of_a + 1]]['objectid']

            if idx_of_a == len(a_actions)-1: 
                a_previous = self.nodes[a_actions[idx_of_a - 1]]['objectid']
                a_nextt = self.nodes[a_actions[idx_of_a]]['objectid']

            else:
                a_previous = self.nodes[a_actions[idx_of_a -1 ]]['objectid']
                a_nextt = self.nodes[a_actions[idx_of_a +1 ]]['objectid']

            # print (idxa, a_name, a_type, a_previous, a_nextt)     
            
            for idxb in b_actions:

                b_name = b.nodes[idxb]['verb']
                
                if 'machine' in b.nodes[idxb].keys():
                    b_type = 'machine'
                    b_child = b.nodes[idxb]['machine']['objectid']
                else: 
                    if 'components' not in b.nodes[idxb] or len(b.nodes[idxb]['components']) == 0:
                        b_type = 'other'
                        b_child = None

                    else: 
                        b_type = 'components'
                        b_child = None
                
                b_parent = b.nodes[idxb].parent['objectid'] # pointer to the step object
                idx_of_b = b_actions.index(idxb)
                
                if idx_of_b == 0: 
                    b_previous = b.nodes[b_actions[idx_of_b]]['objectid']
                    b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

                if idx_of_b == len(b_actions)-1: 
                    b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
                    b_nextt = b.nodes[b_actions[idx_of_b ]]['objectid']

                else:
                    b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
                    b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

                # print (idxb, b_name, b_type, b_previous, b_nextt) 

                #-------- >  LOGIC < ---------------                    

                if a_name == b_name and a_type == b_type:
                    edges = True
                else:
                    edges = False

                if self.nodes[a_previous]['verb'] ==  b.nodes[b_previous]['verb']:
                    previous = True
                else:
                    previous = False

                if self.nodes[a_nextt]['verb'] ==  b.nodes[b_nextt]['verb']:
                    nextt = True
                else:
                    nextt = False   
                
                if edges == True and previous ==True and nextt == True:
                    comparator.append([idxa, idxb, 3])


        return comparator



class Compare(object):
    def __init__(self,protocol_a, protocol_b, **kwargs):
        import pygraphviz as pgv
        import itertools
        self.agraph = pgv.AGraph()
        self.protocol_A = protocol_a
        self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions] # list of actions in pk-objectid format

        self.protocol_B = protocol_b
        self.agraph.graph_attr['clusterrank'] = 'local'
        
        self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]

        if protocol_b == None:
            self.protocol_B = protocol_a
            self.B_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions]
        else:
            self.protocol_B = protocol_b    
            self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]
        # line up matching verbs in the same rank
        # we will add to this function more sophisticated things in the future.

        self.matching_verbs_pk = zip(self.A_pk,self.B_pk)
        self.matching_verbs = zip(self.protocol_A.get_actions, self.protocol_B.get_actions)

    
    def uniqify_order_preserving(self, seq, idfun=None): 
       # order preserving
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result
            


    def align_lists(self,x,y):
        import itertools

        # x = self.protocol_A.get_actions
        # y = self.protocol_B.get_actions
        
        u = list(itertools.chain(*itertools.izip_longest(x,y)))

        if None in u:
            u.pop(u.index(None))

        U = self.uniqify_order_preserving(u)

        out_1 = []

        for i in U:
            if i in x:
                tmpx = i
            else:
                tmpx = None

            if i in y:
                tmpy = i
            else:
                tmpy = None

            out_1.append((tmpx,tmpy))  
        return out_1       

    # def align_lists (self):
    #     import
    #     first = list(self.protocol_A.get_actions)
    #     second = list(self.protocol_B.get_actions)     
    #     len_1 = len(self.protocol_A.get_actions)
    #     len_2 = len(self.protocol_B.get_actions)
    #     if len_1 > len_2:
    #         longer = len_1
    #     else:
    #         longer = len_2

    #     for i in range(longer):
    #         if first[i] == second[i]:
    #             # check that there current sequnce aligns:

    #             continue
    #         else:
    #             # ls2 has an extra action
    #             if first[i] in ls2 and second[i] not in ls1:
    #                 first.insert(i, None) 
    #             if second[i] in ls1 and first[i] not in ls2:
    #                 second.insert(i, None) 

    #     F  = itertools.izip_longest(first,second)
    #     for i, j in F:
    #         print i,j  

    #     return itertools.izip_longest(first,second) 


    def draw_two_protocols(self):
        ''' this function draws out 2 protocols starting with the name of the protocol and then with the nodes 
            add_layers adds the specified layers that a user wants to compare'''

        
            
        for i in range(1, len(self.A_pk)):
            
            self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
            e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = '#B82F3' 
            n=self.agraph.get_node(self.A_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = '20'
            n.attr['style'] = 'rounded'
            n.attr['label']= self.protocol_A.nodes[self.protocol_A.get_actions[i]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[i]].pk

        # Set the 0'th node and title in protocol_A 
        n = self.agraph.get_node(self.matching_verbs_pk[0][0])
        n.attr['shape']='box'
        n.attr['fontsize'] = '20'
        n.attr['style'] = 'rounded'
        n.attr['label']=self.protocol_A.nodes[self.protocol_A.get_actions[0]]['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[0]].pk
        print 'Rendered protocol %s'% self.protocol_A.name
                # add base of second protocol:
        for i in range(1, len(self.B_pk)):
            self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
            print 'drawing protocol %s'% self.protocol_B.name
            e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = '#015666' 
            n=self.agraph.get_node(self.B_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = '20'
            n.attr['style'] = 'rounded'
            n.attr['label']= self.protocol_B.nodes[self.protocol_B.get_actions[i]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[i]].pk

        # Set the 0'th node in  protocol_A  
        n = self.agraph.get_node(self.matching_verbs_pk[0][1])
        n.attr['shape']='box'
        n.attr['fontsize'] = '20'
        n.attr['style'] = 'rounded'
        n.attr['label']=self.protocol_B.nodes[self.protocol_B.get_actions[0]]['verb'] #+ '_' + self.protocol_B.nodes[self.protocol_B.get_actions[0]].pk
        
        ######## # draw cluster around each protocol:#########
        # graph_A = [r for r in self.agraph.nodes() if str(self.protocol_A.pk) in r]
        # graph_B = [r for r in self.agraph.nodes() if str(self.protocol_B.pk) in r]
        # print graph_A, graph_B
        # subgraph_A = self.agraph.add_subgraph(graph_A, name = 'cluster_A', color = '#B82F3') #rank = 'same', rankdir='TD',

        # create the pairwise - verb comparison and return a list of tuples for each verb_a: verb_b match. 

        # for parent,child in self.matching_verbs_pk:
        
        #   rank_list = (parent,child)      
        #   N = self.agraph.add_subgraph(rank_list, rank = 'same', rankdir='LR') #, name='%s'%(layer_names[nc]))
        #   N.edge_attr['color'] = 'white'

        return self.agraph

    def add_diff_layer(self, object_sorting = 'least_errors', **kwargs):
        ''' this function assumes that the pairs of objects are equivalent in that both have validated:
            'machines'
            'components'
            'thermocycle'
            '''

        if 'machine' in kwargs['layers']:
            machines = True
        else:
            machines = False 
        
        if 'component' in kwargs['layers']:
            components = True
        else:
            components = False 
        
        if 'thermo' in kwargs['layers']:
            thermocycle = True
        else:
            thermocycle = False 
                
        for verb_a,verb_b in self.matching_verbs: #[(node_a, node_b), ]
            print verb_a, verb_b
            if 'machine' in self.protocol_A.nodes[verb_a].keys() and machines:  # object has only one child:
                x = self.protocol_A.nodes[verb_a]['machine'].summary
                y = self.protocol_B.nodes[verb_b]['machine'].summary
                d = DictDiffer (x, y)
                content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), machine = True) 

                # trigger = len(d.added()) + len(d.removed()) + len(d.changed(name = True, objectid = True, slug = True))
                # if trigger > 0:
                    
                # --->  create a compare object that will apear between the 2 base diagrams:
                diff_object = self.protocol_A.nodes[verb_a]['machine'].pk
                ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)

                # set all diff objects on same rank:
                # if MACHINE_LAYER:
                #     # add the relevant step layers to the action layers. 
                #     new_rank = 
                #     N = self.agraph.add_subgraph([new_rank], rank = 'same', rankdir = 'LR', name = self.protocol_A.nodes[self.protocol_A.nodes[verb_a].parent['objectid']].pk)#, rankdir='LR')     
                N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', name = self.protocol_A.nodes[verb_a].pk)#, rankdir='LR') 
                
                # set layout and colors
                s = self.agraph.get_node(diff_object)
                s.attr['shape'] = 'box'
                s.attr['color'] = '#C0C0C0'
                s.attr['style'] = 'rounded'

                # set label:
                s.attr['label'] = merge_table_pieces(content)
                
                # --->

            if 'components' in self.protocol_A.nodes[verb_a].keys() and components: # and type(self.protocol_A.nodes[a]) == 'protocols.models.Component':
                # Validate that reagent objectids are the same:


                if len(self.protocol_A.nodes[verb_a]['components']) ==0:
                    continue

                else:
                    components_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
                    components_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                    
                    components_list_diff = set(r['objectid'] for r in self.protocol_A.nodes[verb_a].children) - set(r['objectid'] for r in self.protocol_B.nodes[verb_b].children)

                    if components_list_diff:
                        pass
                        # add a function that can tell the difference between different names
                    
                    else:
                        scores = [] # tracks the error rate of a matching components
                        content = [] # gets the html strings
                        for m,n in zip(components_a,components_b): 
                            d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
                            scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
                            # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
                            tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), components = True) 
                            content.append(tmp)
                            
                    # set the base_graph node:
                    diff_object = self.protocol_A.nodes[components_a[0]].pk 
                    ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                    eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)     
                    N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', name = self.protocol_A.nodes[verb_a].pk) #, name='%s'%(layer_names[nc])) 
                    
                    # set layout and colors
                    s = self.agraph.get_node(diff_object)
                    s.attr['shape'] = 'box'
                    s.attr['color'] = '#C0C0C0'
                    s.attr['style'] = 'rounded'
                    s.attr['label'] = merge_table_pieces(content, 'components')

            if 'thermocycle' in self.protocol_A.nodes[verb_a].keys():
                import itertools
                # get all thermo children:
                phases_A = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
                phases_B = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]

                match = set(phases_A) - set(phases_B)
                if len(match) == 0: 
                    # print 'len match = 0'
                # compare nested thermo objects:
                    table = []
                    for thermo in phases_A:
                        job_A = self.protocol_A.nodes[thermo].summary
                        job_B = self.protocol_B.nodes[thermo].summary
                        # print 'thermo is %s, \n A: %s + \n, B: %s'%(thermo, job_A['name'], job_B['name'])
                        d = DictDiffer(job_A, job_B)
                        if 'phases' in d.changed() or 'cycles' in d.changed():
                            # go through all items in both phases
                            it = itertools.izip(job_A['phases'], job_B['phases']) 
                            
                            for i,j in it: # getting the subphase name that is different
                                subphase_A = i
                                subphase_B = j
                                f = DictDiffer(subphase_A, subphase_B)
                                if f.changed():
                                    L = f.changed() 
                                    
                                    subphases = {}
                                    for each_subphase in L:
                                        # subphases[each_subphase] = [] 
                                        g = DictDiffer(subphase_A[each_subphase], subphase_B[each_subphase])    
                                        subphases[each_subphase] = g.changed()
                                        
                            
                            tmp = add_thermo(job_A, job_B, d.changed(), subphases)
                            table.append(tmp)
                            continue
                
                        if 'name' in d.changed():
                            print 'name changed'    

                        else:
                            tmp = add_thermo(job_A, job_B)
                            table.append(tmp)
                            
                diff_object = self.protocol_A.nodes[phases_A[0]].pk 
                ea = self.agraph.add_edge(self.protocol_A.nodes[verb_a].pk,diff_object)
                eb = self.agraph.add_edge(self.protocol_B.nodes[verb_b].pk,diff_object)     
                N = self.agraph.add_subgraph([self.protocol_A.nodes[verb_a].pk, diff_object, self.protocol_B.nodes[verb_b].pk], rank = 'same', name = self.protocol_A.nodes[verb_a].pk) #, name='%s'%(layer_names[nc])) 
                
                # set layout and colors
                s = self.agraph.get_node(diff_object)
                s.attr['shape'] = 'box'
                s.attr['color'] = '#C0C0C0'
                s.attr['style'] = 'rounded'
                s.attr['label'] = merge_table_pieces(table, 'thermocycle')     
    
        return self.agraph          



def test_compare():
    a  = ProtocolPlot.objects.get(id='3')
    b  = ProtocolPlot.objects.get(id='19')
    G    = Compare(a,b)
    ag  = G.draw_two_protocols()
    af = G.add_diff_layer()
    af.draw('compare/Figures/test.svg', prog = 'dot')
    print 'no errors'
    







    # plot both protocols as the same graph with a separate list of ndoes, use the pk attribute to draw them out. 


            # loop through actions:


    # find verb-type compatabilites
    # determine what type of verb it is: component or machine. 
    #   if both match verb - type make a dim connector add both to the same rank
        ## create a list with [(pk_A, pk_B), 'identical', 'different_keys', 'different_values', url to the same graph with details ]
    #    if they differ in key numbers, change the color of the square
    #  compare both children:
    #   if they match, color both verbs in green 
    #    if they dont, display both, with red highliting the diff and green the black the same
