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
from protocols.utils import MANUAL_VERBS, MACHINE_VERBS, COMPONENT_VERBS, THERMOCYCLER_VERBS, MANUAL_LAYER, settify, labeler 
from compare.utils import MASKS, OUTPUT_MASKS
import itertools
import operator


def union(lists):
    output = set()
    # if len(lists) == 1:
    #     return lists
    for item in lists:
        output = set(output).union(set(item))

    return list(output)        


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    masks: are groupings of keys that can be ignored for the compare. Currently only working for parents. 
    child_eval_method: is a decorator for evaluating and summarizing the keys of children objects. Applying this filter will evaluate the 
    diff using the summary keys and not the original child keys. 
    """


    def __init__(self, data_a, data_b, **kwargs):
        self.data_a, self.data_b = data_a, data_b
        self.set_a, self.set_b = set(data_a.keys()), set(data_b.keys())
        self.intersect = self.set_a.intersection(self.set_b)
    def uniq_a(self):
        return list(self.set_a - self.intersect)
    def uniq_b(self):
        return list(self.set_b - self.intersect)
    def changed(self, **kwargs):
        delta = list(o for o in self.intersect if self.data_b[o] != self.data_a[o])
        return delta
    def unchanged(self):
        return list(o for o in self.intersect if self.data_b[o] == self.data_a[o])

class ColNum(object):
    def __init__(self,colnum):
        self.colnum = colnum
    def __call__(self, x):
        return x[self.colnum]

class ProtocolPlot(Protocol):

    class Meta: 
        proxy = True

    def __init__(self, *args, **kwargs):
        super(ProtocolPlot, self).__init__(*args, **kwargs)

        self.agraph = pgv.AGraph(ranksep = '0.2')  
        self.pks = [self.nodes[r].pk for r in self.get_actions()] # list of actions in pk-objectid format
        
class Compare(object):
    # def __init__(self, protocols, protocol_a, protocol_b = None, **kwargs):
    def __init__(self, protocols, **kwargs):

        self.protocols = protocols
        self.A = protocols[0]
        
        if len(protocols) == 2:
            self.B = protocols[1]
            
        self.aligned = self.align_verbs()            

    def isint(self, x): 
        if type(x) is int:
            return True
        else:
            return False   

    def align_verbs(self):
        '''
        method to align verbs between 2 protocols. to add more protocols to the comaprison, chnage the union command to be recursive 
        '''
        x = self.A.get_actions()
        
        if len(self.protocols) == 1:     
            return x
            
        y = self.B.get_actions()
        r = list(set(x).union(set(y)))
        order = []
        out = []
        for i in r:
            if i in x and i in y:
                order.append((i, x.index(i), y.index(i), x.index(i) + y.index(i)))
            if i in x and i not in y: 
                order.append((i, x.index(i), x.index(i) + 0.5, 2*x.index(i) + 0.5 ))
            if i in y and i not in x: 
                order.append((i, y.index(i) + 0.5, y.index(i), 2*y.index(i) + 0.5)) 

        order.sort(key=ColNum(3))
        
        for row in order:
            if self.isint(row[1]) and self.isint(row[2]):
                out.append((row[0], row[0]))
            if self.isint(row[1]) and not self.isint(row[2]):
                out.append((row[0], None))  
            if self.isint(row[2]) and not self.isint(row[1]):
                out.append((None, row[0]))  
        
        return out          


    def align_protocols_by_object(self, protocol_a, protocol_b, **kwargs):
        '''
        this method takes a compare alignment 
        [('kttj4d', None), ('jhdfs', 'jhdfs')]

        and sends node objects to get added to an AddCompareVerb object. 
        ''' 
        protocols = [protocol_a, protocol_b]
        self.alignment = []
        
        for row in self.aligned:
            line = []
            for (i, obj) in enumerate(row): 
                try:
                    temp = protocols[i].nodes[obj]
                except KeyError:
                    temp = {}

                line.append(temp)   
            self.alignment.append(line) 


    def get_layout_by_object(self, protocols, **kwargs):
        
        self.layout = []
        for row in self.alignment:
            z = CompareVerb()
            z.add_verb_from_protocols(row)
            self.layout.append(z)

    def get_layout_by_objectid(self, **kwargs):
        
        self.layout = []
        if len(self.protocols) >1:
            self.alignment = [next(obj for obj in r if obj) for r in self.aligned]
        else:
             self.alignment = self.aligned   
    
        for objid in self.alignment:
            z = CompareVerb(self.protocols, objid)
            # z.add_verb_from_protocols(objid)
            self.layout.append(z)        
        
class CompareVerb(dict):
    ''' this function take a list of protocols and objectids specified by the parent caller 
    (get_json_align) for all protocols in the comparison. 
        
        '''
    def __init__(self, protocols, objectid, **kwargs):
        self.protocols = protocols
        self.objectid = objectid
        self.children = []
        self.attribs = ['name', 'objectid', 'node_type', 'child_type', 'child_diff', 'child', 'duration']
        for item in self.attribs:
            self[item] = []

    # def add_verb_from_protocols(self, objectid, **kwargs):
        dirty = False
        diff = "False"

        for protocol in self.protocols:
            # if protocol.nodes[objectid]:
            node = self.get_node(protocol, self.objectid)    
            if node:
                self['name'].append(node['name'])
                self['node_type'].append(node.node_type)
                self['objectid'].append(node['objectid'])
                self['duration'].append("None")
                self['child_type'].append(node.childtype())
                
                if node.children:
                    self.children.append([r['objectid'] for r in node.children])
                    dirty = True
                    manual = False
                if node['verb'] in MANUAL_VERBS:
                    self.children.append([self.objectid])                    
                    dirty = True
                    manual = True
                # self['child'].append(self.add_children(node))
            else:
                diff = "True"
                self['name'].append("None")
                self['node_type'].append("None")
                self['objectid'].append("None")
                self['child_type'].append("None")
                self['duration'].append("None")
                self['child_diff'].append(diff)
                self['child'].append([])   

        if dirty:
            self['child'] = self.add_children(manual)  
     
        if len(self.protocols) == 1:
            self['child_diff'] = "False"    
        else:

        ##### ALL THE FILTERING AND MASKING HAPPENS HERE  ###########
            self['child_diff'] = self.child_diff(objectid, diff, masks = MASKS, child_eval_method = True, output_key_masking = None)

        self['node_type'] = next(obj for obj in self['node_type'] if obj)
        self['name'] = next(obj for obj in self['name'] if obj)

    def get_node(self, protocol, objectid, **kwargs):

        try:
            result = protocol.nodes[objectid]
        except KeyError:
            result = None

        if 'true' in kwargs and result:
            return kwargs['true']

        if 'summary' in kwargs.keys() and result:
            return result.summary

        else:
            return result              

    def add_children(self, manual = False, **kwargs):
        
        output = []

        # !!! NEW STUFF!!!
        # all_children = union(self.children)
        all_children = self.align_children(self.children)
        
        
        for child_id in all_children:
            z = CompareChildren(self.protocols, child_id, manual)
            output.append(z)
            
        return output        
        
    def align_children(self, children):
        '''
        method to align verbs between 2 protocols. to add more protocols to the comaprison, chnage the union command to be recursive 
        '''
        x = children[0]
        
        if len(children) == 1:         
            return x
            
        y = children[1]
        r = list(set(x).union(set(y)))
        order = []
        out = []
        for i in r:
            if i in x and i in y:
                order.append((i, x.index(i), y.index(i), x.index(i) + y.index(i)))
            if i in x and i not in y: 
                order.append((i, x.index(i), x.index(i) + 0.5, 2*x.index(i) + 0.5 ))
            if i in y and i not in x: 
                order.append((i, y.index(i) + 0.5, y.index(i), 2*y.index(i) + 0.5)) 

        order.sort(key=ColNum(3))

        for row in order:
            if self.isint(row[1]) and self.isint(row[2]):
                out.append((row[0], row[0]))
            if self.isint(row[1]) and not self.isint(row[2]):
                out.append((row[0], None))  
            if self.isint(row[2]) and not self.isint(row[1]):
                out.append((None, row[0]))  
        
        if len(self.protocols) >1:
            return [next(obj for obj in r if obj) for r in out]         

        return out    

    def isint(self, x): 
        if type(x) is int:
            return True
        else:
            return False 
    def child_diff(self, objectid, prev_diff, display = False, masks = None, child_eval_method = False, output_key_masking = None, **kwargs ):
        '''
        All Filtering  and Masking is perfomred on the eval_node dict, this is the input to DictDiffer. 
        '''
        diff = prev_diff
        
        if len(self.protocols) == 1:
            diff =False
            return diff

        filters = {}
        filters['masks'] = masks
        filters['child_eval_method'] = child_eval_method
        filters['output_key_masking'] = output_key_masking

        comparator = []
        
        for protocol in self.protocols:
            node = self.get_node(protocol, self.objectid)    
            if node:
                eval_node = dict(node)
                # MASK PARENT ATTRIBUTES:
                if filters['masks'] is not None:
                    for item in filters['masks']: 
                        [eval_node.pop(key, None) for key in filters['masks'][item] if key in eval_node.keys()]
                
                # SET CHILD EVALUTAION METHOD:
                if filters['child_eval_method']:
                    if 'manual'in node.childtype():
                        eval_node = node.summary
                    
                    if 'machine'in node.childtype() and 'machine' in eval_node:
                        eval_node['machine'] = node['machine'].summary
                    
                    if 'components'in node.childtype() and 'components' in eval_node:
                        eval_node['components'] = [r.summary for r in node['components']]

                    if 'thermocycle'in node.childtype() and 'thermocycle' in eval_node:
                        eval_node['thermocycle'] = [r.summary for r in node['thermocycle']]
            else:
                eval_node = {}            

            comparator.append(eval_node)            
        
        if len(comparator) == 2:
            #masks = ['experiment','for_deletion','schedule','short_term', 'children_keys'], child_eval_method = 'summary', output_key_masking = True
            D = DictDiffer(comparator[0], comparator[1])
            if len(D.changed()) > 0:
                diff = "True"
                if display:
                    print 'parent:', self.objectid, D.changed()
            if len(D.uniq_a()) > 0:
                diff = "True"    
                if display:
                    print 'parent:', self.objectid, D.uniq_a()
            if len(D.uniq_b()) > 0:
                diff = "True"
                if display:        
                    print 'parent:', self.objectid, D.uniq_b()
            
        
        return diff
        
        
class CompareChildren(CompareVerb):
    ''' this function take a list of protocols and objectids specified by the parent caller 
    (get_json_align) for all protocols in the comparison. 
        
        '''
    def __init__(self, protocols, objectid, manual = False, display = False, **kwargs):
        self.protocols = protocols
        self.objectid = objectid
        self.attribs = ['objectid', 'node_type', 'URL']
        self.nodes = []
        diff = False
        for item in self.attribs:
            self[item] = []
        
        for item in self.get_summary_attributes(manual):
            self[item] = []        

        for i, protocol in enumerate(self.protocols):
            # if protocol.nodes[objectid]:
            node = self.get_node(protocol, self.objectid)    
            # self.nodes.append(self.get_node(protocol, self.objectid, summary = True))
            if node:
                self.nodes.append(self.get_node(protocol, self.objectid, summary = True)) 
                self['node_type'].append(node.node_type)
                self['objectid'].append(node['objectid'])
                if manual:
                    self['URL'].append(node.action_update_url())

                    self['verb'].append(node['name'])
                else:
                    self['URL'].append(node.get_update_url())
                # if 'published' in protocol.status:
                #     self['URL'].append(node.get_absolute_url())
                for item in self.get_summary_attributes():
                    self[item].append(node.summary.get(item, "None"))        
                
            else:
                self['node_type'].append([])
                self['objectid'].append("None")
                self['URL'].append("None")
                for item in self.get_summary_attributes():
                    self[item].append("None")        
        
        
        self['node_type'] = next(obj for obj in self['node_type'] if obj)        
        # if 'link' in self.keys():
        #     del(self['link'])
                        
    def get_summary_attributes(self, manual = False, **kwargs):

        attribs = []
        for protocol in self.protocols:
            node = self.get_node(protocol, self.objectid, summary= True)    
            if node:
                self.nodes.append(node)
                attribs.append(node.keys()) 
                if manual:
                    attribs.append(['verb'])
            
        return union(attribs)   
