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
from compare.utils import html_label_two_protocols, merge_table_pieces, add_step_label #, html_label_one_protocol, add_html_cell, set_title_label,
import itertools
import operator

FONT_SIZE = '10'
HTML_TARGET = '_top'
COLOR_A = '#B82F3'
COLOR_B = '#015666' 
NODE_STYLE = 'solid' # "rounded" produces a longer svg filled with polylines. 


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
        # if 'name' in delta and 'name' in kwargs:
        #     delta.pop(delta.index('name'))
        # if 'objectid' in delta and 'objectid' in kwargs:
        #     delta.pop(delta.index('objectid'))
        if 'slug' in delta and 'slug' in kwargs:
            delta.pop(delta.index('slug'))
        return delta
    def unchanged(self):
        return list(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

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
        # print self.alignment
        for objid in self.alignment:
            z = CompareVerb(self.protocols, objid)
            # z.add_verb_from_protocols(objid)
            self.layout.append(z)        


        
class CompareVerb(dict, Compare):
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
                self['child_diff'].append("True")
                self['child'].append([])   

        if dirty:
            self['child'] = self.add_children(manual)  
     
        if len(self.protocols) == 1:
            self['child_diff'] = "False"    
        else:
            self['child_diff'] = self.child_diff(objectid, diff)

        self['node_type'] = next(obj for obj in self['node_type'] if obj)
        self['name'] = next(obj for obj in self['name'] if obj)

    def get_node(self, protocol, objectid, **kwargs):

        try:
            result = protocol.nodes[objectid]
        except KeyError:
            result = None

        if 'true' in kwargs and result:
            return kwargs['true']
        else:
            return result              

    def add_children(self, manual = False, **kwargs):
        
        output = []

        # !!! NEW STUFF!!!
        # all_children = union(self.children)
        all_children = self.align_children(self.children)
        
        # print 'union of all children:', all_children
        for child_id in all_children:
            z = CompareChildren(self.protocols, child_id, manual)
            output.append(z)
            
        return output        
        
    # !!! NEW STUFF!!!
    def align_children(self, children):
        '''
        method to align verbs between 2 protocols. to add more protocols to the comaprison, chnage the union command to be recursive 
        '''
        x = children[0]
        
        if len(self.protocols) == 1:     
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
            self.alignment = [next(obj for obj in r if obj) for r in out]         

        return out    


    def child_diff(self, objectid, prev_diff, **kwargs):
        diff = prev_diff

        node1 = self.get_node(self.protocols[0], self.objectid)    
        node2 = self.get_node(self.protocols[1], self.objectid)    
        
        if len(self.protocols) == 1:
            return False
        
        if node1 and node2: 
            D = DictDiffer(node1, node2)
            if len(D.changed()) > 0:
                diff = "True"

            if len(D.uniq_a()) > 0:
                diff = "True"    

            if len(D.uniq_b()) > 0:
                diff = "True"        

        return diff
        
        
class CompareChildren(CompareVerb):
    ''' this function take a list of protocols and objectids specified by the parent caller 
    (get_json_align) for all protocols in the comparison. 
        
        '''
    def __init__(self, protocols, objectid, manual = False, **kwargs):
        self.protocols = protocols
        self.objectid = objectid
        self.attribs = ['objectid', 'node_type', 'URL']
        for item in self.attribs:
            self[item] = []
        
        for item in self.get_summary_attributes(manual):
            self[item] = []        

        for protocol in self.protocols:
            # if protocol.nodes[objectid]:
            node = self.get_node(protocol, self.objectid)    
            if node:
                 
                self['node_type'].append(node.node_type)
                print (node['name'], node['objectid'], manual)
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
            node = self.get_node(protocol, self.objectid)    
            if node:
                attribs.append(node.summary.keys()) 
                if manual:
                    attribs.append(['verb'])
        print union(attribs)            
        return union(attribs)   

# if node['name'] in MANUAL_VERBS:
        #     temp_child = {}
        #     children_a = self.A.summary.keys()

            
        #     self.both = list(set(children_a).union(set(children_b)))                    
        #     for fchild in self.both:
        #         temp_child[fchild] = [protocol_a.nodes[objectid].get(fchild, "None"), protocol_b.nodes[objectid].get(fchild, "None")]

        #     self['child'].append(temp_child)        









# class AddCompareVerbs(dict):
#     def __init__(self, protocol_a, protocol_b, objectid, **kwargs):
#         '''        
#         CompareVerbs takes an objectid and compares it between the N protocols. 
#         The object returns a dict with attributes to be considered or displayed in a visual diff. 
#         the diff method indicates wheather items should be drawn in two separate boxes or in one box. 
#         '''
#         self.A = self.get_node(protocol_a, objectid)
#         self.B = self.get_node(protocol_b, objectid)
#         # B = self.get_node(protocol_b, objectid) 

#         temp_name = [protocol_a.get_item(objectid, 'name'), protocol_b.get_item(objectid, 'name')]
#         self['name'] = next(obj for obj in temp_name if obj)

#         temp_node_type = [protocol_a.get_item(objectid, 'object_type'), protocol_b.get_item(objectid, 'object_type')]  

#         self['node_type'] = next(obj for obj in temp_node_type if obj)
        
#         self['objectid'] = [protocol_a.get_item(objectid, 'objectid'), protocol_b.get_item(objectid, 'objectid')]
        

#     def add_to_verb(self, protocol_a, protocol_b, objectid, **kwargs):
        

#         if self.A and self.B:    
#             self['child_type'] = [protocol_a.get_item(objectid, 'childtype'), protocol_b.get_item(objectid, 'childtype')]                
#             # self['duration'] = [protocol_a.get_item(objectid, 'duration')[0], protocol_b.get_item(objectid, 'duration')[0]]
#             self['duration'] = [protocol_a.nodes[objectid].get('duration', "None"), protocol_b.nodes[objectid].get('duration', "None")]
            
#             diff = (self.A, self.B)
#             self.diff = diff 

#             D = DictDiffer(protocol_a.nodes[objectid], protocol_b.nodes[objectid])
#             if len(D.changed()) > 0:
#                 item = next(obj for obj in diff if obj)    
#                 if item.childtype() in D.changed():
#                     self['child_diff'] = True
#                 else:
#                     self['child_diff'] = False

#         if self.A and not self.B:             
#             self['child_type'] = [protocol_a.get_item(objectid, 'childtype'), None]                
#                 # self['duration'] = [protocol_a.get_item(objectid, 'duration')[0], protocol_b.get_item(objectid, 'duration')[0]]
#             self['duration'] = [protocol_a.nodes[objectid].get('duration', "None"), protocol_b.nodes[objectid].get('duration', "None")]
                
#             diff = (self.A, self.B)
#             self.diff = diff 

#             D = DictDiffer(protocol_a.nodes[objectid], protocol_b.nodes[objectid])
#             if len(D.changed()) > 0:
#                 item = next(obj for obj in diff if obj)    
#                 if item.childtype() in D.changed():
#                     self['child_diff'] = True
#                 else:
#                     self['child_diff'] = False  


#             # this should automatically add the values to all the keys / methods / properties 
#             # and not return a KeyError. this is a basic method that can be used for verb and 
#             # children objects. 
#             # Sequence: this 
        
#             # self.diff = diff 

#     def get_children(self, protocol_a, protocol_b, objectid, **kwargs):
#         # self['child'] = []
#         children_a = []
#         children_b = []
        
#         if self['name'] in MANUAL_VERBS:
#             temp_child = {}
#             if self.A:
#                 children_a = self.A.summary.keys()

#             if self.B:
#                 children_b = self.B.summary.keys()    

#             self.both = list(set(children_a).union(set(children_b)))                    
#             for fchild in self.both:
#                 temp_child[fchild] = [protocol_a.nodes[objectid].get(fchild, "None"), protocol_b.nodes[objectid].get(fchild, "None")]

#             self['child'].append(temp_child)        

#         else:       
#             if self.A:    
#                 children_a = [r['objectid'] for r in self.A.children]

#             if self.B:
#                 children_b = [r['objectid'] for r in self.B.children]
            
#             self.bothids = list(set(children_a).union(set(children_b)))                    
#             for childids in self.bothids:
#                 self['child'].append(AddCompareChildren(protocol_a, protocol_b, childids))
        

# def get_node(self, protocol, objectid, **kwargs):
    
#     try:
#         result = protocol.nodes[objectid]
#     except KeyError:
#         result = None

#     if 'true' in kwargs and result:
#         return kwargs['true']
#     else:
#         return result      











# class AddCompareChildren(AddCompareVerbs):
#     def __init__(self, protocol_a, protocol_b, objectid, **kwargs):
        
#         super(AddCompareChildren, self).__init__(protocol_a, protocol_b, objectid, **kwargs)
#         # import pdb; pdb.set_trace()
#         '''
#         CompareChildren takes an objectid and compares it between the 2 protocols. 
#         The object returns a dict with attributes to be displayed in a visual diff. 
#         the diff method indicates wheather items should be drawn in two separate boxes or in one box. 
#         '''
        
#         diff = False
        
#         self['objectid'] = [protocol_a.get_item(objectid, 'objectid'), protocol_b.get_item(objectid, 'objectid')]  
#         # self['objectid'] =
#         A = self.get_node(protocol_a, objectid)
#         B = self.get_node(protocol_b, objectid)
#         # set URL function:
#         if A:
#             A_url = getattr(protocol_a.nodes[A.parent['objectid']], 'action_update_url')()        
#             if 'Published' in protocol_a.status:
#                 A_url = getattr(protocol_a.nodes[A.parent['objectid']], 'get_absolute_url')()    
#         else:
#             A_url = None        

#         if B:
#             B_url = getattr(protocol_b.nodes[B.parent['objectid']], 'action_update_url')()    
#             if 'Published' in protocol_b.status:
#                 B_url = getattr(protocol_b.nodes[B.parent['objectid']], 'get_absolute_url')()
#         else:
#             B_url = None        

#         self['URL'] = [A_url, B_url]    

#         if A and B:    
            
#             summary_items = list(set(A.summary).union(set(B.summary)))
#             D = DictDiffer(A.summary, B.summary)
#             if len(D.changed()) > 0:
#                 diff = True 
#             for item in summary_items:
#                 self[item] = [A.summary.get(item, "None"), B.summary.get(item, "None")] 

#         if A and not B:    
#             summary_items = A.summary.keys()
#             diff = True
#             for item in summary_items:
#                 self[item] = [A.summary.get(item, "None"), "None"] 
        
#         if B and not A:    
#             summary_items = B.summary.keys()    
#             diff = True
#             for item in summary_items:
#                 self[item] = ["None", B.summary.get(item, "None")] 

            
#         self.diff = diff







    
# __________________________________________________________________________________________    
    # def find_diff_verbs(self, **kwargs):

    #     # A = self.protocol_A
    #     # B = self.protocol_B
    #     # verbs = list(set(A.get_actions()).union(set(B.get_actions())))

    #     diffs = []
    #     for verb in self.align_verbs():
    #         if None in verb:
    #             diffs.append((verb, []))
    #         else:
    #             D = DictDiffer(self.protocol_A.nodes[verb[0]], self.protocol_B.nodes[verb[1]])
    #             changed = D.changed()
    #             uniqs_a = D.uniq_a()
    #             uniqs_b = D.uniq_b()
                
    #             diff_attributes = []
    #             dirty = False

    #             if changed:
    #                 diff_attributes.append(changed)
    #                 dirty = True
    #             if uniqs_a:
    #                 diff_attributes.append(added)
    #                 dirty = True
    #             if uniqs_b:
    #                 diff_attributes.append(removed)
    #                 dirty = True

    #             if dirty:    
    #                 attributes = [item for sublist in diff_attributes for item in sublist]
    #                 diffs.append((verb, attributes))        

    #     return diffs          

    # def get_diff_alignment(self, **kwargs):

    #     # A = self.protocol_A
    #     # B = self.protocol_B
    #     # verbs = list(set(A.get_actions()).union(set(B.get_actions())))

    #     diffs = []
    #     for verb in self.align_verbs():
    #         if None in verb:
    #             diffs.append((verb, []))
    #         else:
    #             D = DictDiffer(self.protocol_A.nodes[verb[0]], self.protocol_B.nodes[verb[1]])
    #             changed = D.changed()
    #             uniqs_a = D.uniq_a()
    #             uniqs_b = D.uniq_b()
                
    #             diff_attributes = []
    #             dirty = False

    #             if changed:
    #                 diff_attributes.append(changed)
    #                 dirty = True
    #             if uniqs_a:
    #                 diff_attributes.append(uniqs_a)
    #                 dirty = True
    #             if uniqs_b:
    #                 diff_attributes.append(uniqs_b)
    #                 dirty = True
                    
    #             attributes = [item for sublist in diff_attributes for item in sublist]
    #             diffs.append((verb, attributes))        

    #     return diffs              

    # def get_aligned_diff_object(self, **kwargs):
        
    #     out = []
    #     # dirty = False
    #     child_nodes = ['machine', 'components', 'thermocycle']
    #     diff = self.find_diff_verbs()
    #     for obj in diff:
    #         dirty = False
    #         if None in obj[0]:
    #             dirty = True
    #             if not obj[0][0]:
    #                 protocol = self.protocol_B 
    #                 objid = obj[0][1]
    #             else:
    #                 protocol = self.protocol_A
    #                 objid = obj[0][0]
    #         else:
    #             protocol = self.protocol_A
    #             objid = obj[0][0]
            
    #         node_dict = self.get_diff_attributes(obj)
    #         node_dict['node_type'] = "Action"
    #         node_dict['name'] = protocol.nodes[objid]['name']
    #         node_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #         node_dict['verb_objectid'] = obj[0]
    #         node_dict['child_type'] = protocol.nodes[objid].childtype()
    #         if node_dict['child_type'] in child_nodes:
    #             if dirty:
    #                 nodes = protocol.nodes[objid].children
    #                 node_dict['child'] = [r.summary for r in protocol.nodes[objid].children]
    #             else:    
    #                 node_dict['child'] = self.get_child_diff(objid)

    #         out.append(node_dict)

    #     return out 



    # def get_aligned_protocols(self, **kwargs):
        
    #     out = []
    #     # dirty = False
    #     child_nodes = ['machine', 'components', 'thermocycle']
    #     diff = self.get_diff_alignment()
    #     for obj in diff:
    #         dirty = False
    #         if None in obj[0]:
    #             dirty = True
    #             if not obj[0][0]:
    #                 protocol = self.protocol_B 
    #                 objid = obj[0][1]
    #             else:
    #                 protocol = self.protocol_A
    #                 objid = obj[0][0]
    #         else:
    #             protocol = self.protocol_A
    #             objid = obj[0][0]
            
    #         node_dict = self.get_diff_attributes(obj)
    #         node_dict['node_type'] = "Action"
    #         node_dict['name'] = protocol.nodes[objid]['name']
    #         # node_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #         node_dict['objectid'] = obj[0]
    #         node_dict['child_type'] = protocol.nodes[objid].childtype()
    #         node_dict['child_diff'] = False
    #         print str(protocol.nodes[objid].childtype())
    #         print obj[1]
    #         print str(protocol.nodes[objid].childtype()) in obj[1]
    #         if str(protocol.nodes[objid].childtype()) in obj[1]:
    #             node_dict['child_diff'] = True                
        
    #         if node_dict['child_type'] in child_nodes:
    #             if dirty:
    #                 print 
    #                 nodes = protocol.nodes[objid].children
    #                 node_dict['child'] = [r.summary for r in protocol.nodes[objid].children]
    #             else:    
    #                 node_dict['child'] = self.get_child_diff(objid)

    #         out.append(node_dict)

    #     return out     

    
    # def get_diff_attributes(self, obj, **kwargs):
    #     '''obj: ((objectid_a, objectid_b), [attributes])'''

    #     child_nodes = ['machine', 'components', 'thermocycle']
    #     exclude = ['duration', u'physical_commitment']
    #     exclude_all = child_nodes + exclude
    #     out = {}
    #     non_children_attributes = list(set(obj[1])-set(exclude_all))
        


    #     for attr in non_children_attributes:
    #         out[attr] = [getattr(self.protocol_A.nodes[obj[0][0]], attr), getattr(self.protocol_B.nodes[obj[0][1]], attr)]

    #     return out    

    # def get_child_diff(self, parent_id, **kwargs):
    #     ''' this method is called knowing that the parent_id has children
    #     '''
        
    #     out = []
    #     children_a = self.protocol_A.nodes[parent_id].children # either one or more children
    #     children_b = self.protocol_B.nodes[parent_id].children

        
    #     children_A = [r['objectid'] for r in self.protocol_A.nodes[parent_id].children if self.protocol_A.nodes[parent_id].childtype() is not None ]
    #     children_B = [r['objectid'] for r in self.protocol_B.nodes[parent_id].children if self.protocol_B.nodes[parent_id].childtype() is not None ]
        
    #     both = list(set(children_A).intersection(set(children_B)))    
    #     unique_A = list(set(children_A)-set(children_B))
    #     unique_B = list(set(children_B)-set(children_A)) 
        
    #     if len(both) == 1:
    #         temp = self.child_compare(0, both[0])        
    #         if temp:
    #             out.append(temp)
            
    #     if len(both) > 1:
    #         for (cnt, item) in enumerate(both):    
    #             temp = self.child_compare(cnt, item) 
    #             if temp:
    #                 out.append(temp)

    #     if len(unique_A) == 1:
    #         temp = self.child_dict(0, unique_A[0], side = 'LEFT')
    #         if temp:
    #             out.append(temp)
            
    #     if len(unique_A) > 1:
    #         for (cnt, item) in enumerate(unique_A):    
    #             temp = self.child_dict(cnt, item, side = 'LEFT') 
    #             if temp:
    #                 out.append(temp)

    #     if len(unique_B) == 1:
    #         temp = self.child_dict(0, unique_B[0], side = 'RIGHT')
    #         if temp:
    #             out.append(temp)
            
    #     if len(unique_B) > 1:
    #         for (cnt, item) in enumerate(unique_B):    
    #             temp = self.child_dict(cnt, item, side = 'RIGHT') 
    #             if temp:
    #                 out.append(temp)                                
    #     return out             
        
    
    # def child_compare(self, cnt, item, **kvargs):    
    #     dirty = False
    #     child_dict={}
    #     LEFT = self.protocol_A
    #     RIGHT = self.protocol_B
    #     # child_dict['order'] = str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype()) + ' ' + str(cnt)
        
    #     child_dict['name'] =  [LEFT.nodes[item]['name'], RIGHT.nodes[item]['name']] 
    #     child_dict['node_type'] =  str(LEFT.nodes[LEFT.nodes[item].parent['objectid']].childtype())
    #     child_dict['number'] =  child_dict['node_type'] + ' ' + str(cnt)
    #     child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #     child_dict['node_objectid'] = LEFT.nodes[item]['objectid']
    #     D = DictDiffer(LEFT.nodes[item].summary, RIGHT.nodes[item].summary)
        
    #     for attr in D.changed():  
    #         if len(D.changed()) > 0:
    #             dirty = True
    #             child_dict[attr] = [LEFT.nodes[item].summary[attr],RIGHT.nodes[item].summary[attr]]
    
    #     for attr in D.uniq_a():
    #         if len(D.uniq_a()) > 0:    
    #             dirty = True
    #             child_dict[attr] = [LEFT.nodes[item].summary[attr],None]

    #     for attr in D.uniq_b():
    #         if len(D.uniq_b()) > 0:    
    #             dirty = True
    #             child_dict[attr] = [None, RIGHT.nodes[item].summary[attr]]    

    #     if dirty:
    #         return child_dict        
    #     else:
    #         return {}    

    # def child_dict(self, cnt, item, side = None):
    #     child_dict={}
    #     if side == 'LEFT':
    #         protocol = self.protocol_A
    #     if side == 'RIGHT': 
    #         protocol = self.protocol_B
            
    #     child_dict['name'] =  protocol.nodes[item]['name']
    #     child_dict['node_type'] =  str(protocol.nodes[protocol.nodes[item].parent['objectid']].childtype())
    #     child_dict['number'] =  child_dict['node_type'] + ' ' + str(cnt)
    #     child_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #     child_dict['node_objectid'] = protocol.nodes[item]['objectid']
    #     # if side == 'LEFT':
    #     for attr in protocol.nodes[item].summary:
    #         child_dict[attr] = [protocol.nodes[item].summary[attr], None]
    #     # if side == 'RIGHT':
    #     #     for attr in self.protocol_B.nodes[item].summary:        
    #     #         child_dict[attr] = [None, self.protocol_B.nodes[item].summary[attr]]                      

    #     return child_dict        


    # def get_node_dict(self, obj, **kwargs):
    #     out = {}
    #     node_dict = self.get_diff_attributes(obj)



    # def get_diff_attributes_all_protocol(self, **kwargs):

    #     # !!! doesn't work for childless verb!!!
    #     child_nodes = ['machine', 'components', 'thermocycle']
    #     attributes = self.find_diff_verbs()
    #     # non_children_attributes = list(set(attributes)-set(child_nodes))

    #     out = {}
    #     for obj in attributes:
    #         non_children_attributes = list(set(obj[1])-set(child_nodes))
    #         for attr in non_children_attributes:
    #             out[attr] = [self.protocol_A.nodes[obj[0]][attr],self.protocol_B.nodes[obj[0]][attr]]

    #     return out            

    # def make_diff_object(self, **kwargs):
        
    #     out = []
    #     child_nodes = ['machine', 'components', 'thermocycle']
    #     diff = self.find_diff_verbs()
    #     for obj in diff:
    #         node_dict = self.get_diff_attributes(obj)
    #         node_dict['node'] = "verb"
    #         node_dict['name'] = self.protocol_A.nodes[obj[0]]['name']
    #         node_dict['diff_objectid'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #         node_dict['node_objectid'] = self.protocol_A.nodes[obj[0]]['objectid']
    #         node_dict['child_type'] = self.protocol_A.nodes[obj[0]].childtype()
    #         if node_dict['child_type'] in child_nodes:
    #             node_dict['child'] = self.get_child_diff(obj[0])

    #         out.append(node_dict)

    #     return out
    


    # def draw_two_protocols(self, **kwargs):
    #     ''' this function draws out 2 base protocols as a sequence of actions. 
    #         add_layers_routine(layers = 'none-manual') adds the specified layers that a user wants to compare'''

    #     # Draw out the first protocol:
    #     self.layers = []    
    #     for i in range(1, len(self.A_pk)):
            
    #         self.agraph.add_edge(self.A_pk[i-1], self.A_pk[i])
    #         e = self.agraph.get_edge(self.A_pk[i-1], self.A_pk[i])
    #         e.attr['style'] = 'setlinewidth(9)' 
    #         e.attr['color'] = COLOR_A
    #         n=self.agraph.get_node(self.A_pk[i])
    #         n.attr['shape']='box'
    #         n.attr['fontsize'] = FONT_SIZE
    #         n.attr['style'] = NODE_STYLE
    #         n.attr['height'] = '0.2'
    #         node_object = self.protocol_A.nodes[self.protocol_A.get_actions()[i]]
    #         n.attr['label']= node_object['verb'] #+ '_' + self.protocol_A.nodes[self.protocol_A.get_actions()[i]].pk
    #         # n.attr['URL'] = node_object.get_absolute_url()
    #         # n.attr['target'] = HTML_TARGET
                
    #     # Set the 0'th node and title in protocol_A 
    #     n = self.agraph.get_node(self.A_pk[0])
    #     n.attr['shape']='box'
    #     n.attr['fontsize'] = FONT_SIZE
    #     n.attr['style'] = NODE_STYLE
    #     n.attr['height'] = '0.2'
    #     node_object = self.protocol_A.nodes[self.protocol_A.get_actions()[0]]
    #     n.attr['label']=node_object['verb'] 
    #     # n.attr['URL'] = node_object.get_absolute_url()
    #     # n.attr['target'] = HTML_TARGET
        
    #     # add base of second protocol:
    #     for i in range(1, len(self.B_pk)):
    #         self.agraph.add_edge(self.B_pk[i-1], self.B_pk[i])
    #         # print 'drawing protocol %s'% self.protocol_B.name
    #         e = self.agraph.get_edge(self.B_pk[i-1], self.B_pk[i])
    #         e.attr['style'] = 'setlinewidth(9)' 
    #         e.attr['color'] = COLOR_B
    #         n=self.agraph.get_node(self.B_pk[i])
    #         n.attr['shape']='box'
    #         n.attr['fontsize'] = FONT_SIZE
    #         n.attr['style'] = NODE_STYLE
    #         n.attr['height'] = '0.2'
    #         node_object = self.protocol_B.nodes[self.protocol_B.get_actions()[i]]
    #         n.attr['label']= node_object['verb'] 
    #         # n.attr['URL'] = node_object.get_absolute_url()    
    #         # n.attr['target'] = HTML_TARGET
    #     # Set the 0'th node in  protocol_A  
    #     n = self.agraph.get_node(self.B_pk[0])
    #     n.attr['shape']='box'
    #     n.attr['fontsize'] = FONT_SIZE
    #     n.attr['style'] = NODE_STYLE
    #     n.attr['height'] = '0.2'
    #     node_object = self.protocol_B.nodes[self.protocol_B.get_actions()[0]]
    #     n.attr['label']= node_object['verb'] 
    #     # n.attr['URL'] = node_object.get_absolute_url()
    #     # n.attr['target'] = HTML_TARGET

    #     for j in self.pairs:
    #         N = self.agraph.add_subgraph(j, name =str(j[0][j[0].index('-')+1:]), rank='same', rankdir='LR')
    
    #     # return self

    
    # def add_layers_routine(self, **kwargs):
    #     ''' this function adds layers on the three groups of subgraphs that control the verb alignment in this view: 
    #     paired --> verb_a.pk -- diff_object.pk -- verb_b.pk
    #     single_left --> verb_a.pk -- diff_object.pk 
    #     single_right -->  diff_object.pk -- verb_b.pk
    #     it currently adds these layers:
    #         'manual',
    #         'machines'
    #         'components'
    #         'thermocycle'
    #         'steps' - displays verbatim text. '''

    #     if 'layers' in kwargs.keys():
    #         self.layers = kwargs['layers'].split('-')

    #     self.add_node_object(self.both, ref_protocol = self.protocol_A)

    #     # these lists contain a few or no nodes:
    #     if self.a_unique:
    #         self.flags['position'] = 'right'
    #         self.add_node_object(self.a_unique, ref_protocol = self.protocol_A, position = 'right')
    #     if self.b_unique:
    #         self.flags['position'] = 'left'
    #         self.add_node_object(self.b_unique, ref_protocol = self.protocol_B, position = 'left')


    # def add_node_object(self, node_group, ref_protocol = None, **kwargs): # , machines = True, components = True, thermocycle = True
        
    #     if 'position' in kwargs:
    #         pass

    #     for j in node_group:
    #         # identify the type of layer
    #         if 'machine' in ref_protocol.nodes[j] and 'machine' in self.layers:
    #             if not self.add_machine_layer(j, ref_protocol):
    #                 continue

    #         if ref_protocol.nodes[j]['verb'] in MANUAL_VERBS and 'manual' in self.layers:    
    #             if not self.add_manual_layer(j, ref_protocol):
    #                 continue

    #         if 'components' in ref_protocol.nodes[j] and 'components' in self.layers:     
    #             if not self.add_components_layer(j, ref_protocol):
    #                 continue

    #         if 'thermocycle' in ref_protocol.nodes[j] and 'thermo' in self.layers:                 
    #             if not self.add_thermocycle_layer(j, ref_protocol):
    #                 continue

    # def add_machine_layer(self, j, ref_protocol):
    #     layer = 'machine'
    #     node_object = ref_protocol.nodes[j]['machine']
    #     URL = node_object.get_update_url()
    #     diff_object = ref_protocol.nodes[j]['machine'].pk
    #     if 'position' in self.flags:
    #         if self.flags['position'] == 'right':
    #             x = ref_protocol.nodes[j]['machine'].summary
    #             y = x

    #         if self.flags['position'] == 'left':
    #             y =  ref_protocol.nodes[j]['machine'].summary   
    #             x = y
        
    #     else: 
    #         x = self.protocol_A.nodes[j]['machine'].summary
    #         y = self.protocol_B.nodes[j]['machine'].summary
        
    #     d = DictDiffer (x, y)
    #     content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer = layer) 
    #     self.style_content(j, URL, diff_object, content)

    # def add_manual_layer(self, j, ref_protocol):
    #     layer = 'manual'
    #     node_object = ref_protocol.nodes[j]
    #     URL = node_object.action_update_url()
    #     diff_object = ref_protocol.nodes[j].pk + '_manual'
    #     if 'position' in self.flags:
    #         if self.flags['position'] == 'right':
    #             x = ref_protocol.nodes[j].summary
    #             y = x

    #         if self.flags['position'] == 'left':
    #             y =  ref_protocol.nodes[j].summary   
    #             x = y    
        
    #     else:        
    #         x = self.protocol_A.nodes[j].summary
    #         y = self.protocol_B.nodes[j].summary  
        
    #     d = DictDiffer (x, y)
    #     content = html_label_two_protocols(x,y,d.changed(name = True, objectid = True, slug = True), d.unchanged(), current_layer=layer)   
    #     self.style_content(j, URL, diff_object, content)

    # def add_components_layer(self, j, ref_protocol):
    #     layer = 'components'

    #     # Validate that reagent objectids are the same:

    #     if len(ref_protocol.nodes[j]['components']) == 0:
    #         return None
    #     else:
    #         node_object = ref_protocol.nodes[j]
    #         URL ='None'

    #         if 'position' in self.flags:
    #             if self.flags['position'] == 'right':
    #                 x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
    #                 y = x

    #             if self.flags['position'] == 'left':
    #                 y = [r['objectid'] for r in self.protocol_B.nodes[j].children] 
    #                 x = y 

    #         else:        
    #         # generate the diff content:   
    #             x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
    #             y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
    #         diff_object = ref_protocol.nodes[x[0]].pk 
    #         scores = [] # tracks the error rate of a matching components
    #         content = [] # gets the html strings
    #         for m,n in zip(x,y): 
    #             d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
    #             scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
    #             # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
    #             tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
    #             content.append(tmp)      
            
    #         self.style_content(j, URL, diff_object, content, current_layer = layer)    

    # def add_thermocycle_layer(self, j, ref_protocol):
    #     layer = 'thermocycle'
    #     if len(ref_protocol.nodes[j]['thermocycle']) == 0:
    #         return None
    #     else:
    #         # generate the diff content:   
    #         x = [r['objectid'] for r in self.protocol_A.nodes[j].children]
    #         y = [r['objectid'] for r in self.protocol_B.nodes[j].children]
            
    #         scores = [] # tracks the error rate of a matching components
    #         content = [] # gets the html strings
    #         for m,n in zip(x,y): 
    #             d = DictDiffer (self.protocol_A.nodes[m].summary, self.protocol_B.nodes[n].summary)
    #             scores.append((len(d.added()) + len(d.removed()) + len(d.changed())))
    #             # print self.protocol_A.nodes[m]['objectid'], self.protocol_A.nodes[n]['objectid'], d.changed()
    #             tmp = html_label_two_protocols(self.protocol_A.nodes[m].summary,self.protocol_B.nodes[n].summary,d.changed(), d.unchanged(), current_layer = layer) 
    #             content.append(tmp)

    #         diff_object = ref_protocol.nodes[x[0]].pk 
    #         URL = None
    #         self.style_content(j, URL, diff_object, content, current_layer = layer)  

    #     # for j in self.a_unique:               
                    

                
    # def style_content(self, j, URL, diff_object, content, current_layer = None):

    #     try:
    #         N = self.agraph.get_subgraph(str(j))
    #         if len(N.nodes()) == 2:
    #             (verb_object_a, verb_object_b) = N.nodes()
    #             N.add_node(diff_object)        
    #             self.agraph.add_edge(verb_object_a,diff_object)
    #             self.agraph.add_edge(diff_object, verb_object_b)    

    #     except AttributeError:
    #         if self.flags['position'] == 'right':
    #             verb_object_a = self.protocol_A.nodes[j].pk
    #             self.agraph.add_edge(verb_object_a,diff_object)
    #             subgraph = [verb_object_a, diff_object]

    #         if self.flags['position'] == 'left':    
    #             verb_object_b = self.protocol_B.nodes[j].pk
    #             self.agraph.add_edge(diff_object, verb_object_b)
    #             subgraph = [diff_object, verb_object_b]

    #         N = self.agraph.add_subgraph(subgraph, name =str(j), rank='same', rankdir='LR')    
          
    #     s = self.agraph.get_node(diff_object)
    #     s.attr['shape'] = 'box'
    #     s.attr['color'] = '#C0C0C0'
    #     s.attr['style'] = NODE_STYLE
    #     s.attr['fontsize'] = FONT_SIZE  

    #     # set label:
    #     s.attr['label'] = merge_table_pieces(content, current_layer)

    #     # if current_layer == 'manual':
    #     #     node_object = self.protocol_A.nodes[j]
    #     #     s.attr['URL'] = node_object.action_update_url()

    #     # else:
    #     #     node_object = self.protocol_A.nodes[j][current_layer]
    #     #     s.attr['URL'] = node_object.get_update_url()    
    #     s.attr['URL'] = URL

    #     s.attr['target'] = HTML_TARGET      



    

    




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

    #     # x = self.protocol_A.get_actions()
    #     # y = self.protocol_B.get_actions()
        
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
    #     first = list(self.protocol_A.get_actions())
    #     second = list(self.protocol_B.get_actions())     
    #     len_1 = len(self.protocol_A.get_actions())
    #     len_2 = len(self.protocol_B.get_actions())
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

    # def plot(self, **kwargs):
    #     # super(ProtocolPlot, self).__init__(**kwargs)
    #     # self.prot = Protocol.objects.get(name__icontains=protocol_name)
        
    #     for i in range(1, len(self.pks)):
    #         self.agraph.add_edge(self.pks[i-1],self.pks[i])
    #         e = self.agraph.get_edge(self.pks[i-1], self.pks[i])
    #         e.attr['style'] = 'setlinewidth(9)' 
    #         e.attr['color'] = '#B82F3' 
    #         n=self.agraph.get_node(self.pks[i])
    #         n.attr['shape']='box'
    #         n.attr['fontsize'] = '10'
    #         n.attr['style'] = NODE_STYLE
    #         n.attr['height'] = '0.2'
    #         n.attr['label']= self.nodes[self.get_actions()[i]]['verb']

    #     n = self.agraph.get_node(self.pks[0])
    #     n.attr['shape']='box'
    #     n.attr['fontsize'] = '10'
    #     n.attr['style'] = NODE_STYLE
    #     n.attr['height'] = '0.2'
    #     n.attr['label']=self.nodes[self.get_actions()[0]]['verb']

