import string
import random
from django.db import models
import pygraphviz as pgv 
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel
from protocols.utils import MANUAL_VERBS
from compare.utils import html_label_two_protocols, merge_table_pieces, add_step_label #, html_label_one_protocol, add_html_cell, set_title_label,
import itertools

FONT_SIZE = '10'
HTML_TARGET = '_top'
COLOR_A = '#B82F3'
COLOR_B = '#015666' 
NODE_STYLE = 'solid' # "rounded" produces a longer svg filled with polylines. 


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
    def uniq_a(self):
        return list(self.set_current - self.intersect)
    def uniq_b(self):
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
            n.attr['style'] = NODE_STYLE
            n.attr['height'] = '0.2'
            n.attr['label']= self.nodes[self.get_actions[i]]['verb']

        n = self.agraph.get_node(self.pks[0])
        n.attr['shape']='box'
        n.attr['fontsize'] = '10'
        n.attr['style'] = NODE_STYLE
        n.attr['height'] = '0.2'
        n.attr['label']=self.nodes[self.get_actions[0]]['verb']
        

class Compare(object):
    def __init__(self, protocol_a, protocol_b = None, format="svg", **kwargs):
        import pygraphviz as pgv

        self.agraph = pgv.AGraph(ranksep = '0.2')
        self.agraph.graph_attr['clusterrank'] = 'local' # do not remove this line
        self.protocol_A = protocol_a
        self.A_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions]
        self.flags = {}
        
        if protocol_b == None:
            self.protocol_B = protocol_a
            self.B_pk = [self.protocol_A.nodes[r].pk for r in self.protocol_A.get_actions]
            self.flags['steps'] = True
        else:
            self.protocol_B = protocol_b    
            self.B_pk = [self.protocol_B.nodes[r].pk for r in self.protocol_B.get_actions]
            self.flags['steps'] = False

        # find all actions common to both protocols:    
        self.both = list(set(self.protocol_A.get_actions).intersection(set(self.protocol_B.get_actions)))
        # alls = set(self.protocol_A.get_actions).union(set(self.protocol_B.get_actions))
        # Set the pair names using the .pk index for graph node naming
        self.pairs = [(self.protocol_A.nodes[r].pk, self.protocol_B.nodes[r].pk) for r in self.both]
        # set the unaligned verbs:
        self.a_unique = set(self.protocol_A.get_actions)-set(self.protocol_B.get_actions)
        self.b_unique = set(self.protocol_B.get_actions)-set(self.protocol_A.get_actions)
        
    
    def find_diff_verbs(self, **kwargs):

        diffs = []
        for verb in self.both:
            D = DictDiffer(self.protocol_A.nodes[verb], self.protocol_B.nodes[verb])
            changed = D.changed()
            uniqs_a = D.uniq_a()
            uniqs_b = D.uniq_b()
            
            diff_attributes = []
            dirty = False

            if changed:
                diff_attributes.append(changed)
                dirty = True
            if uniqs_a:
                diff_attributes.append(added)
                dirty = True
            if uniqs_b:
                diff_attributes.append(removed)
                dirty = True

            if dirty:    
                attributes = [item for sublist in diff_attributes for item in sublist]
                diffs.append((verb, attributes))        

        return diffs      

    def get_diff_attributes_all_protocol(self, **kwargs):
        child_nodes = ['machine', 'components', 'thermocycle']
        attributes = self.find_diff_verbs()
        # non_children_attributes = list(set(attributes)-set(child_nodes))

        out = {}
        for obj in attributes:
            print 'object=', obj
            non_children_attributes = list(set(obj[1])-set(child_nodes))
            print 'non_ca: ', non_children_attributes
            for attr in non_children_attributes:
                print 'attribute: ', attr
                out[attr] = [self.protocol_A.nodes[obj[0]][attr],self.protocol_B.nodes[obj[0]][attr]]

        return out  

    def get_diff_attributes(self, obj, **kwargs):
        child_nodes = ['machine', 'components', 'thermocycle']
        attributes = self.find_diff_verbs()
        # non_children_attributes = list(set(attributes)-set(child_nodes))

        out = {}
        non_children_attributes = list(set(obj[1])-set(child_nodes))
        print 'non_ca: ', non_children_attributes
        for attr in non_children_attributes:
            print 'attribute: ', attr
            out[attr] = [self.protocol_A.nodes[obj[0]][attr],self.protocol_B.nodes[obj[0]][attr]]

        return out          

    def make_diff_object(self, **kwargs):
        
        out = []
        child_nodes = ['machine', 'components', 'thermocycle']
        diff = self.find_diff_verbs()
        for obj in diff:
            # attributes = get_diff_attributes(obj)
            node_dict = self.get_diff_attributes(obj)

            node_dict['node'] = "verb"
            node_dict['name'] = self.protocol_A.nodes[obj[0]]['name']
            node_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            node_dict['node_objectid'] = self.protocol_A.nodes[obj[0]]['objectid']
            node_dict['child_type'] = self.protocol_A.nodes[obj[0]].childtype()
            if node_dict['child_type'] in child_nodes:
                node_dict['child'] = self.get_child_diff(obj[0])

            out.append(node_dict)

        return out    


    def get_child_diff(self, parent_id, **kwargs):
        ''' this method is called knowing that the parent_id has children
        '''
        
        out = []
        children_a = self.protocol_A.nodes[parent_id].children # either one or more children
        children_b = self.protocol_B.nodes[parent_id].children

        if type(children_a) is list: 
            children_A = [r['objectid'] for r in self.protocol_A.nodes[parent_id].children if self.protocol_A.nodes[parent_id].childtype() is not None ]
        else:
            children_A = [children_a['objectid']]
            
        if type(children_b) is list:      
            children_B = [r['objectid'] for r in self.protocol_B.nodes[parent_id].children if self.protocol_B.nodes[parent_id].childtype() is not None ]
        else:
            children_B = [children_b['objectid']]

        both = list(set(children_A).intersection(set(children_B)))    
        unique_A = list(set(children_A)-set(children_B))
        unique_B = list(set(children_B)-set(children_A)) 
        
        if len(both) == 1:
            temp = self.child_compare(0, both[0])        
            if temp:
                out.append(temp)
            
        if len(both) > 1:
            for (cnt, item) in enumerate(both):    
                temp = self.child_compare(cnt, item) 
                if temp:
                    out.append(temp)

        if len(unique_A) == 1:
            temp = self.child_dict(0, unique_A[0], side = 'LEFT')
            if temp:
                out.append(temp)
            
        if len(unique_A) > 1:
            for (cnt, item) in enumerate(unique_A):    
                temp = self.child_dict(cnt, item, side = 'LEFT') 
                if temp:
                    out.append(temp)

        if len(unique_B) == 1:
            temp = self.child_dict(0, unique_B[0], side = 'RIGHT')
            if temp:
                out.append(temp)
            
        if len(unique_B) > 1:
            for (cnt, item) in enumerate(unique_B):    
                temp = self.child_dict(cnt, item, side = 'RIGHT') 
                if temp:
                    out.append(temp)                                
        return out             
        
    
    def child_compare(self, cnt, item, **kvargs):    
        dirty = False
        child_dict={}
        LEFT = self.protocol_A
        RIGHT = self.protocol_B
        # child_dict['order'] = str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype()) + ' ' + str(cnt)
        child_dict['node'] =  str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype())
        child_dict['number'] =  child_dict['node'] + ' ' + str(cnt)
        child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        child_dict['node_objectid'] = LEFT.nodes[item]['objectid']
        D = DictDiffer(LEFT.nodes[item].summary, RIGHT.nodes[item].summary)
        
        for attr in D.changed():  
            if len(D.changed()) > 0:
                dirty = True
                child_dict[attr] = [LEFT.nodes[item].summary[attr],RIGHT.nodes[item].summary[attr]]
    
        for attr in D.uniq_a():
            if len(D.uniq_a()) > 0:    
                dirty = True
                child_dict[attr] = [LEFT.nodes[item].summary[attr],None]

        for attr in D.uniq_b():
            if len(D.uniq_b()) > 0:    
                dirty = True
                child_dict[attr] = [None, RIGHT.nodes[item].summary[attr]]    

        if dirty:
            return child_dict        
        else:
            return {}    

    def child_dict(self, cnt, item, side = None):
        child_dict={}
        if side == 'LEFT':
            protocol = self.protocol_A
        if side == 'RIGHT': 
            protocol = self.protocol_B
            
        child_dict['node'] =  str(protocol.nodes[protocol.nodes[item].parent['objectid']].childtype())
        child_dict['number'] =  child_dict['node'] + ' ' + str(cnt)
        child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
        child_dict['node_objectid'] = protocol.nodes[item]['objectid']
        # if side == 'LEFT':
        for attr in protocol.nodes[item].summary:
            child_dict[attr] = [protocol.nodes[item].summary[attr], None]
        # if side == 'RIGHT':
        #     for attr in self.protocol_B.nodes[item].summary:        
        #         child_dict[attr] = [None, self.protocol_B.nodes[item].summary[attr]]                      

        return child_dict        



    def draw_two_protocols(self, **kwargs):
        ''' this function draws out 2 base protocols as a sequence of actions. 
            add_layers_routine(layers = 'none-manual') adds the specified layers that a user wants to compare'''

        # Draw out the first protocol:
        self.layers = []    
        for i in range(1, len(self.A_pk)):
            
            self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
            e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = COLOR_A
            n=self.agraph.get_node(self.A_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = FONT_SIZE
            n.attr['style'] = NODE_STYLE
            n.attr['height'] = '0.2'
            node_object = self.protocol_A.nodes[self.protocol_A.get_actions[i]]
            n.attr['label']= node_object['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions[i]].pk
            # n.attr['URL'] = node_object.get_absolute_url()
            # n.attr['target'] = HTML_TARGET
                
        # Set the 0'th node and title in protocol_A 
        n = self.agraph.get_node(self.A_pk[0])
        n.attr['shape']='box'
        n.attr['fontsize'] = FONT_SIZE
        n.attr['style'] = NODE_STYLE
        n.attr['height'] = '0.2'
        node_object = self.protocol_A.nodes[self.protocol_A.get_actions[0]]
        n.attr['label']=node_object['verb'] 
        # n.attr['URL'] = node_object.get_absolute_url()
        # n.attr['target'] = HTML_TARGET
        
        # add base of second protocol:
        for i in range(1, len(self.B_pk)):
            self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
            # print 'drawing protocol %s'% self.protocol_B.name
            e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
            e.attr['style'] = 'setlinewidth(9)' 
            e.attr['color'] = COLOR_B
            n=self.agraph.get_node(self.B_pk[i])
            n.attr['shape']='box'
            n.attr['fontsize'] = FONT_SIZE
            n.attr['style'] = NODE_STYLE
            n.attr['height'] = '0.2'
            node_object = self.protocol_B.nodes[self.protocol_B.get_actions[i]]
            n.attr['label']= node_object['verb'] 
            # n.attr['URL'] = node_object.get_absolute_url()    
            # n.attr['target'] = HTML_TARGET
        # Set the 0'th node in  protocol_A  
        n = self.agraph.get_node(self.B_pk[0])
        n.attr['shape']='box'
        n.attr['fontsize'] = FONT_SIZE
        n.attr['style'] = NODE_STYLE
        n.attr['height'] = '0.2'
        node_object = self.protocol_B.nodes[self.protocol_B.get_actions[0]]
        n.attr['label']= node_object['verb'] 
        # n.attr['URL'] = node_object.get_absolute_url()
        # n.attr['target'] = HTML_TARGET

        for j in self.pairs:
            N = self.agraph.add_subgraph(j, name =str(j[0][j[0].index('-')+1:]), rank='same', rankdir='LR')
    
        # return self

    
    def add_layers_routine(self, **kwargs):
        ''' this function adds layers on the three groups of subgraphs that control the verb alignment in this view: 
        paired --> verb_a.pk -- diff_object.pk -- verb_b.pk
        single_left --> verb_a.pk -- diff_object.pk 
        single_right -->  diff_object.pk -- verb_b.pk
        it currently adds these layers:
            'manual',
            'machines'
            'components'
            'thermocycle'
            'steps' - displays verbatim text. '''

        if 'layers' in kwargs.keys():
            self.layers = kwargs['layers'].split('-')

        self.add_node_object(self.both, ref_protocol = self.protocol_A)

        # these lists contain a few or no nodes:
        if self.a_unique:
            self.flags['position'] = 'right'
            self.add_node_object(self.a_unique, ref_protocol = self.protocol_A, position = 'right')
        if self.b_unique:
            self.flags['position'] = 'left'
            self.add_node_object(self.b_unique, ref_protocol = self.protocol_B, position = 'left')


    def add_node_object(self, node_group, ref_protocol = None, **kwargs): # , machines = True, components = True, thermocycle = True
        
        if 'position' in kwargs:
            pass

        for j in node_group:
            # identify the type of layer
            if 'machine' in ref_protocol.nodes[j] and 'machine' in self.layers:
                if not self.add_machine_layer(j, ref_protocol):
                    continue

            if ref_protocol.nodes[j]['verb'] in MANUAL_VERBS and 'manual' in self.layers:    
                if not self.add_manual_layer(j, ref_protocol):
                    continue

            if 'components' in ref_protocol.nodes[j] and 'components' in self.layers:     
                if not self.add_components_layer(j, ref_protocol):
                    continue

            if 'thermocycle' in ref_protocol.nodes[j] and 'thermo' in self.layers:                 
                if not self.add_thermocycle_layer(j, ref_protocol):
                    continue

    def add_machine_layer(self, j, ref_protocol):
        layer = 'machine'
        node_object = ref_protocol.nodes[j]['machine']
        URL = node_object.get_update_url()
        diff_object = ref_protocol.nodes[j]['machine'].pk
        if 'position' in self.flags:
            if self.flags['position'] == 'right':
                x = ref_protocol.nodes[j]['machine'].summary
                y = x

            if self.flags['position'] == 'left':
                y =  ref_protocol.nodes[j]['machine'].summary   
                x = y
        
        else: 
            x = self.protocol_A.nodes[j]['machine'].summary
            y = self.protocol_B.nodes[j]['machine'].summary
        
        d = DictDiffer (x, y)
        content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer = layer) 
        self.style_content(j, URL, diff_object, content)

    def add_manual_layer(self, j, ref_protocol):
        layer = 'manual'
        node_object = ref_protocol.nodes[j]
        URL = node_object.action_update_url()
        diff_object = ref_protocol.nodes[j].pk + '_manual'
        if 'position' in self.flags:
            if self.flags['position'] == 'right':
                x = ref_protocol.nodes[j].summary
                y = x

            if self.flags['position'] == 'left':
                y =  ref_protocol.nodes[j].summary   
                x = y    
        
        else:        
            x = self.protocol_A.nodes[j].summary
            y = self.protocol_B.nodes[j].summary  
        
        d = DictDiffer (x, y)
        content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer=layer)   
        self.style_content(j, URL, diff_object, content)

    def add_components_layer(self, j, ref_protocol):
        layer = 'components'

        # Validate that reagent objectids are the same:

        if len(ref_protocol.nodes[j]['components']) == 0:
            return None
        else:
            node_object = ref_protocol.nodes[j]
            URL ='None'

            if 'position' in self.flags:
                if self.flags['position'] == 'right':
                    x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
                    y = x

                if self.flags['position'] == 'left':
                    y = [r['objectid'] for r in self.protocol_B.nodes[j].children] 
                    x = y 

            else:        
            # generate the diff content:   
                x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
                y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
            diff_object = ref_protocol.nodes[x[0]].pk 
            scores = [] # tracks the error rate of a matching components
            content = [] # gets the html strings
            for m,n in zip(x,y): 
                d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
                scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
                # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
                tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
                content.append(tmp)      
            
            self.style_content(j, URL, diff_object, content, current_layer = layer)    

    def add_thermocycle_layer(self, j, ref_protocol):
        layer = 'thermocycle'
        if len(ref_protocol.nodes[j]['thermocycle']) == 0:
            return None
        else:
            # generate the diff content:   
            x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
            y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
            scores = [] # tracks the error rate of a matching components
            content = [] # gets the html strings
            for m,n in zip(x,y): 
                d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
                scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
                # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
                tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
                content.append(tmp)

            diff_object = ref_protocol.nodes[x[0]].pk 
            URL = None
            self.style_content(j, URL, diff_object, content, current_layer = layer)  

        # for j in self.a_unique:               
                    

                
    def style_content(self, j, URL, diff_object, content, current_layer = None):

        try:
            N = self.agraph.get_subgraph(str(j))
            if len(N.nodes()) == 2:
                (verb_object_a, verb_object_b) = N.nodes()
                N.add_node(diff_object)        
                self.agraph.add_edge(verb_object_a,diff_object)
                self.agraph.add_edge(diff_object, verb_object_b)    

        except AttributeError:
            if self.flags['position'] == 'right':
                verb_object_a = self.protocol_A.nodes[j].pk
                self.agraph.add_edge(verb_object_a,diff_object)
                subgraph = [verb_object_a, diff_object]

            if self.flags['position'] == 'left':    
                verb_object_b = self.protocol_B.nodes[j].pk
                self.agraph.add_edge(diff_object, verb_object_b)
                subgraph = [diff_object, verb_object_b]

            N = self.agraph.add_subgraph(subgraph, name =str(j), rank='same', rankdir='LR')    
          
        s = self.agraph.get_node(diff_object)
        s.attr['shape'] = 'box'
        s.attr['color'] = '#C0C0C0'
        s.attr['style'] = NODE_STYLE
        s.attr['fontsize'] = FONT_SIZE  

        # set label:
        s.attr['label'] = merge_table_pieces(content, current_layer)

        # if current_layer == 'manual':
        #     node_object = self.protocol_A.nodes[j]
        #     s.attr['URL'] = node_object.action_update_url()

        # else:
        #     node_object = self.protocol_A.nodes[j][current_layer]
        #     s.attr['URL'] = node_object.get_update_url()    
        s.attr['URL'] = URL

        s.attr['target'] = HTML_TARGET      



    

    




#_________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________
    # def uniqify_order_preserving(self, seq, idfun=None): 
    #    # order preserving
    #    if idfun is None:
    #        def idfun(x): return x
    #    seen = {}
    #    result = []
    #    for item in seq:
    #        marker = idfun(item)
    #        if marker in seen: continue
    #        seen[marker] = 1
    #        result.append(item)
    #    return result
            


    # def align_lists(self,x,y):
    #     import itertools

    #     # x = self.protocol_A.get_actions
    #     # y = self.protocol_B.get_actions
        
    #     u = list(itertools.chain(*itertools.izip_longest(x,y)))

    #     if None in u:
    #         u.pop(u.index(None))

    #     U = self.uniqify_order_preserving(u)

    #     out_1 = []

    #     for i in U:
    #         if i in x:
    #             tmpx = i
    #         else:
    #             tmpx = None

    #         if i in y:
    #             tmpy = i
    #         else:
    #             tmpy = None

    #         out_1.append((tmpx,tmpy))  
    #     return out_1       

    # def check_aligned(lst1, lst2):
    #     it = iter(lst1)
    #     try:
    #         i = next(it)
    #         for x in lst2:
    #             if x == i:
    #                 i = next(it)
    #     except StopIteration:
    #         return True
    #     return False    
# http://stackoverflow.com/questions/8024052/comparing-element-order-in-python-lists?answertab=oldest#tab-top
# http://www.avatar.se/molbioinfo2001/dynprog/dynamic.html
# http://www.dzone.com/snippets/needleman-wunsch-back-track

# def add_diff_layer(self, **kwargs): # , machines = True, components = True, thermocycle = True
    #     ''' this function assumes that the pairs of objects are equivalent in that both have validated:
    #         'machines'
    #         'components'
    #         'thermocycle'
    #         'steps' - displays verbatim text. '''
        
    #     if 'layers' in kwargs.keys():
    #         layers = kwargs['layers'].split('-')

    #     if 'steps' in layers: 
    #         first_actions_a = [self.protocol_A.nodes[r].children[0]['objectid'] for r in self.protocol_A.get_steps]
    #         first_actions_b = [self.protocol_A.nodes[r].children[0]['objectid'] for r in self.protocol_B.get_steps]
            
    #         for verb_a,verb_b in self.matching_verbs:

    #             self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
    #             self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
    #             verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
    #             verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

    #             if verb_a in first_actions_a: 

    #                 self.agraph.add_node(self.protocol_A.nodes[self.protocol_A.nodes[verb_a].parent['objectid']].pk)
    #                 self.agraph.add_node(self.protocol_B.nodes[self.protocol_B.nodes[verb_b].parent['objectid']].pk)
    #                 step_object_a = self.agraph.get_node(self.protocol_A.nodes[self.protocol_A.nodes[verb_a].parent['objectid']].pk)
    #                 step_object_b = self.agraph.get_node(self.protocol_B.nodes[self.protocol_B.nodes[verb_b].parent['objectid']].pk)

    #                 self.agraph.add_edge(step_object_a,verb_object_a)
    #                 self.agraph.add_edge(step_object_b,verb_object_b)

    #                 eas = self.agraph.get_edge(step_object_a, verb_object_a)
    #                 ebs = self.agraph.get_edge(step_object_b, verb_object_b)

    #                 N = self.agraph.add_subgraph([step_object_a, verb_object_a, verb_object_b, step_object_b], rank = 'same', rankdir='LR')#) #, name='%s'%(layer_names[nc])) name = self.protocol_A.nodes[verb_a].pk, 
                    
    #                 sa = self.agraph.get_node(step_object_a)
    #                 sa.attr['shape'] = 'box'
    #                 sa.attr['color'] = '#C0C0C0'
    #                 sa.attr['style'] = NODE_STYLE
    #                 sa.attr['fontsize'] = FONT_SIZE
    #                 try:
    #                     VERBATIM_A = self.protocol_A.nodes[verb_a].parent['verbatim_text'] 
    #                 except KeyError:
    #                     VERBATIM_A = 'nothing to show' 
    #                 sa.attr['label'] = add_step_label(VERBATIM_A)
    #                 node_object = self.protocol_A.nodes[verb_a].parent
    #                 sa.attr['URL'] = node_object.step_update_url()
    #                 sa.attr['target'] = HTML_TARGET

    #                 sb = self.agraph.get_node(step_object_b)
    #                 sb.attr['shape'] = 'box'
    #                 sb.attr['color'] = '#C0C0C0'
    #                 sb.attr['style'] = NODE_STYLE
    #                 sb.attr['fontsize'] = FONT_SIZE
    #                 try:
    #                     VERBATIM_B = self.protocol_B.nodes[verb_b].parent['verbatim_text']
    #                 except KeyError:
    #                     VERBATIM_B = 'nothing to show'
    #                 sb.attr['label'] = add_step_label(VERBATIM_B)

    #     for verb_a,verb_b in self.matching_verbs: 
            
    #         if 'machine' in self.protocol_A.nodes[verb_a].keys() and 'machine' in layers:
    #             x = self.protocol_A.nodes[verb_a]['machine'].summary
    #             y = self.protocol_B.nodes[verb_b]['machine'].summary
    #             d = DictDiffer (x, y)
    #             content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), machine = True) 


    #             self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
    #             self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
    #             verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
    #             verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

    #             diff_object = self.protocol_A.nodes[verb_a]['machine'].pk
    #             self.agraph.add_edge(verb_object_a,diff_object)
    #             self.agraph.add_edge(verb_object_b,diff_object)

    #             N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
    #                        # set layout and colors
    #             s = self.agraph.get_node(diff_object)
    #             s.attr['shape'] = 'box'
    #             s.attr['color'] = '#C0C0C0'
    #             s.attr['style'] = NODE_STYLE
    #             s.attr['fontsize'] = FONT_SIZE
    #             # set label:
    #             s.attr['label'] = merge_table_pieces(content)
    #             node_object = self.protocol_A.nodes[verb_a]['machine']
    #             s.attr['URL'] = node_object.get_update_url()
    #             s.attr['target'] = HTML_TARGET

    #         if 'manual' in layers and not self.protocol_A.nodes[verb_a].children:

    #             x = self.protocol_A.nodes[verb_a].summary
    #             y = self.protocol_B.nodes[verb_b].summary
    #             d = DictDiffer (x, y)
    #             content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), manual = True) 


    #             self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
    #             self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
    #             verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
    #             verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

    #             diff_object = self.protocol_A.nodes[verb_a].pk + '_manual'
    #             self.agraph.add_edge(verb_object_a,diff_object)
    #             self.agraph.add_edge(verb_object_b,diff_object)

    #             N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
    #                        # set layout and colors
    #             s = self.agraph.get_node(diff_object)
    #             s.attr['shape'] = 'note'
    #             s.attr['color'] = '#C0C0C0'
    #             s.attr['height'] = '0.18'
    #             s.attr['fontsize'] = FONT_SIZE
    #             # set label:
    #             s.attr['label'] = merge_table_pieces(content)
    #             node_object = self.protocol_A.nodes[verb_a]
    #             s.attr['URL'] = node_object.action_update_url()
    #             s.attr['target'] = HTML_TARGET    

    #         if 'components' in self.protocol_A.nodes[verb_a].keys() and 'component' in layers: 
    #             # Validate that reagent objectids are the same:


    #             if len(self.protocol_A.nodes[verb_a]['components']) == 0:
    #                 continue
    #             else:
    #                 # generate the diff content:   
    #                 components_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
    #                 components_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                    
    #                 components_list_diff = set(r['objectid'] for r in self.protocol_A.nodes[verb_a].children) - set(r['objectid'] for r in self.protocol_B.nodes[verb_b].children)

    #                 if components_list_diff:
    #                     pass
    #                     # add a function that can tell the difference between different names
                    
    #                 else:
    #                     scores = [] # tracks the error rate of a matching components
    #                     content = [] # gets the html strings
    #                     for m,n in zip(components_a,components_b): 
    #                         d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
    #                         scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
    #                         # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
    #                         tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), components = True) 
    #                         content.append(tmp)
                            
    #                 # --->  create a compare-graph-object that will apear between the 2 base diagrams:
    #                 self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
    #                 self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
    #                 verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
    #                 verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

    #                 diff_object = self.protocol_A.nodes[components_a[0]].pk 
    #                 ea = self.agraph.add_edge(verb_object_b, diff_object)
    #                 eb = self.agraph.add_edge(verb_object_a, diff_object)     
                
    #                 N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc]))     
    #                 # set layout and colors
    #                 s = self.agraph.get_node(diff_object)
    #                 s.attr['shape'] = 'box'
    #                 s.attr['color'] = '#C0C0C0'
    #                 s.attr['style'] = NODE_STYLE
    #                 s.attr['fontsize'] = FONT_SIZE
    #                 s.attr['label'] = merge_table_pieces(content, 'components')
    #                 s.attr['target'] = HTML_TARGET
    #                 # node_object = self.protocol_A.nodes[verb_a]['components']
    #                 # s.attr['URL'] = node_object.get_update_url()
                    

    #         if 'thermocycle' in self.protocol_A.nodes[verb_a].keys() and 'thermo' in layers: 

    #             if len(self.protocol_A.nodes[verb_a]['thermocycle']) == 0:
    #                 continue
    #             else:
    #                 # generate the diff content:   
    #                 thermo_a = [r['objectid'] for r in self.protocol_A.nodes[verb_a].children]
    #                 thermo_b = [r['objectid'] for r in self.protocol_B.nodes[verb_b].children]
                    
    #                 scores = [] # tracks the error rate of a matching components
    #                 content = [] # gets the html strings
    #                 for m,n in zip(thermo_a,thermo_b): 
    #                     d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
    #                     scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
    #                     # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
    #                     tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), thermocycle = True) 
    #                     content.append(tmp)
                            
    #                 # --->  create a compare-graph-object that will apear between the 2 base diagrams:
    #                 self.agraph.add_node(self.protocol_A.nodes[verb_a].pk)
    #                 self.agraph.add_node(self.protocol_B.nodes[verb_b].pk)
    #                 verb_object_a = self.agraph.get_node(self.protocol_A.nodes[verb_a].pk)
    #                 verb_object_b = self.agraph.get_node(self.protocol_B.nodes[verb_b].pk)

    #                 diff_object = self.protocol_A.nodes[thermo_a[0]].pk 
    #                 ea = self.agraph.add_edge(verb_object_b, diff_object)
    #                 eb = self.agraph.add_edge(verb_object_a, diff_object)     
                    
    #                 N = self.agraph.add_subgraph([verb_object_a, diff_object, verb_object_b], rank = 'same', name = self.protocol_A.nodes[verb_a].pk, rankdir='LR')#) #, name='%s'%(layer_names[nc])) 
    #                 # set layout and colors
    #                 s = self.agraph.get_node(diff_object)
    #                 s.attr['shape'] = 'box'
    #                 s.attr['color'] = '#C0C0C0'
    #                 s.attr['style'] = NODE_STYLE
    #                 s.attr['fontsize'] = FONT_SIZE
    #                 s.attr['label'] = merge_table_pieces(content, 'thermocycle')
    #                 # node_object = self.protocol_A.nodes[verb_a]['thermocycle']
    #                 # s.attr['URL'] = node_object.get_update_url()
    #                 # s.attr['target'] = HTML_TARGET
       
    #     return self 



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

# def same_rank_objects_by_1st_degree_nbrs(self, protocol_B):


#         # a = ProtocolPlot.objects.get(name__icontains=protocol_A)  
#         b = ProtocolPlot.objects.get(name__icontains=protocol_B)
        
#         a_actions = [r[2] for r in self.get_action_tree('objectid')]
#         b_actions = [r[2] for r in b.get_action_tree('objectid')]

    
#         comparator = []

#         for idxa in a_actions:
            
#             a_name = self.nodes[idxa]['verb']
#             if 'machine' in self.nodes[idxa].keys():
#                 a_type = 'machine'
#                 a_child = self.nodes[idxa]['machine']['objectid']
#             # if 'components' in self.nodes[idxa].keys():
#             else: 
#                 if 'components' not in self.nodes[idxa] or len(self.nodes[idxa]['components']) == 0:
#                     a_type = 'other'
#                     a_child = None

#                 else: 
#                     a_type = 'components'
#                     a_child = [r['objectid'] for r in self.nodes[idxa]['components']]
            
#             a_parent = self.nodes[idxa].parent['objectid'] # pointer to the step object
#             idx_of_a = a_actions.index(idxa)
            
#             if idx_of_a == 0: 
#                 a_previous = self.nodes[idxa]['objectid']
#                 a_nextt = self.nodes[a_actions[idx_of_a + 1]]['objectid']

#             if idx_of_a == len(a_actions)-1: 
#                 a_previous = self.nodes[a_actions[idx_of_a - 1]]['objectid']
#                 a_nextt = self.nodes[a_actions[idx_of_a]]['objectid']

#             else:
#                 a_previous = self.nodes[a_actions[idx_of_a -1 ]]['objectid']
#                 a_nextt = self.nodes[a_actions[idx_of_a +1 ]]['objectid']

#             # print (idxa, a_name, a_type, a_previous, a_nextt)     
            
#             for idxb in b_actions:

#                 b_name = b.nodes[idxb]['verb']
                
#                 if 'machine' in b.nodes[idxb].keys():
#                     b_type = 'machine'
#                     b_child = b.nodes[idxb]['machine']['objectid']
#                 else: 
#                     if 'components' not in b.nodes[idxb] or len(b.nodes[idxb]['components']) == 0:
#                         b_type = 'other'
#                         b_child = None

#                     else: 
#                         b_type = 'components'
#                         b_child = None
                
#                 b_parent = b.nodes[idxb].parent['objectid'] # pointer to the step object
#                 idx_of_b = b_actions.index(idxb)
                
#                 if idx_of_b == 0: 
#                     b_previous = b.nodes[b_actions[idx_of_b]]['objectid']
#                     b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

#                 if idx_of_b == len(b_actions)-1: 
#                     b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
#                     b_nextt = b.nodes[b_actions[idx_of_b ]]['objectid']

#                 else:
#                     b_previous = b.nodes[b_actions[idx_of_b -1 ]]['objectid']
#                     b_nextt = b.nodes[b_actions[idx_of_b +1 ]]['objectid']

#                 # print (idxb, b_name, b_type, b_previous, b_nextt) 

#                 #-------- >  LOGIC < ---------------                    

#                 if a_name == b_name and a_type == b_type:
#                     edges = True
#                 else:
#                     edges = False

#                 if self.nodes[a_previous]['verb'] ==  b.nodes[b_previous]['verb']:
#                     previous = True
#                 else:
#                     previous = False

#                 if self.nodes[a_nextt]['verb'] ==  b.nodes[b_nextt]['verb']:
#                     nextt = True
#                 else:
#                     nextt = False   
                
#                 if edges == True and previous ==True and nextt == True:
#                     comparator.append([idxa, idxb, 3])


#         return comparator
#     