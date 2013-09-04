from protocols.forms import verbs as verb_forms
from protocols.forms import forms
import time

import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_verb_list():
    verb_list = []
    for attr_name in dir(verb_forms):
        form_candidate = getattr(verb_forms, attr_name, None)
        try:
            if issubclass(form_candidate, forms.Form):
                verb_list.append(form_candidate)
        except TypeError:
            continue
    return verb_list


VERB_LIST = get_verb_list()
VERB_CHOICES = [(x.slug, x.name) for x in VERB_LIST]
VERB_FORM_DICT = {x.slug: x for x in VERB_LIST}

MACHINE_VERBS = [x.slug for x in VERB_LIST if x.has_machine]
COMPONENT_VERBS = [x.slug for x in VERB_LIST if x.has_component]
THERMOCYCLER_VERBS = [x.slug for x in VERB_LIST if x.has_thermocycler]
MANUAL_VERBS = [x.slug for x in VERB_LIST if x.has_manual]
MANUAL_LAYER = dict((x.slug, x.layers) for x in VERB_LIST if x.layers)

# MANUAL_LAYER={'mix':['technique_comment','duration','duration_units'],
#                 'place':['item_to_place','target','conditional_statement','technique_comment','duration','duration_units'],
#                 'discard':['item_to_discard','item_to_retain','conditional_statement','technique_comment','duration','duration_units'],
#                 'let-sit-stand':'settify',
#                 'store':'settify',
#                 'transfer':['item_to_place','old_vessel','new_vessel','item_to_discard','technique_comment','min_vol','vol_units','duration','duration_units'],
#                 'dry':['technique_comment'],
#                 }

def settify(settings_dict, shorthand = True, summary = False, action = False, comments = False):

    settings = []
    units = ''
    output = {}
    
    # Duration replaces min_time if None, or not present. 


    # if 'duration' in settings_dict:
    #     if 'min_time' not in settings_dict or not settings_dict['min_time']:
    #         settings_dict['min_time'] = settings_dict['duration']

    # if 'duration_units' in settings_dict:
    #     if 'time_units' not in settings_dict or not settings_dict['time_units']: 
    #         settings_dict['time_units'] = settings_dict['duration_units']            

    items = ['temp', 'time', 'speed', 'cycle', 'comment', 'conc', 'vol', 'mass', 'link', 'technique']

    for item in items:
        data = dict((k, v) for k, v in settings_dict.iteritems() if item in k and v != None)
        if not data:
            continue
        if item == 'cycle':
            units = None
            numbers = None
            out = None
            
            plural = ' cycles'

            if 'cycle_back_to' in data and 'cycles' in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
                cycle_to = data['cycle_back_to'] 

            if 'cycles' in data and 'cycle_back_to' not in data:
                if data['cycles'] == '1':
                    plural = ' cycle'
                
                numbers = str(data['cycles']) 
                units = plural
            if summary:
                output['cycles'] = numbers
                output['cycle_back_to'] = data.get('cycle_back_to', None)
            else:    
                settings.append(out)

        if item == 'link':
            if summary:
                output['link'] = data['protocol_link']        

        if item == 'technique':
            if 'technique_comment' in settings_dict:
                output['technique_comment'] = settings_dict['technique_comment']

                
        else:        
            max_item = 'max_' + item
            min_item = 'min_' + item  
            unit_item = item + '_units'
            comment_item = item + '_comment'
            units = None
            numbers = None
            out = None

            if max_item in data and min_item in data:
                if data[max_item] == data[min_item]:
                    # units_c = conc['max_conc']
                    numbers = str(data[max_item])
                else:
                    # units_c = data[min_item] + '-' + data[max_item]
                    numbers = str(data[min_item]) + '-' + str(data[max_item])
            else:
                if max_item in data:
                     # units_c = conc[max_item]
                    numbers = str(data[max_item])
                if min_item in data:
                     # units_c = conc[min_item]   
                    numbers = str(data[min_item]) 

            if numbers != None:
                
                if unit_item in data:
                    units = str(data[unit_item])
                else:
                    units = ''
                    # return 'no concentration units specified for %s' % units_dict['name']
                out = str(numbers) + ' ' + units
                    
                if comment_item in data:
                    comment = str(data[comment_item])
                else:
                    comment = None

                if shorthand:
                    units = shorten(units)           

                if comment:
                    output[item] = [numbers, units, comment]

                if summary:
                    output[item] = [numbers, units]    
                else:    
                    settings.append(out)
             
    if summary:
        return output
    else:
        return settings        


def shorten(units):

    d ={'nanograms':'ng',
        'micrograms':'ug',    
        'milligrams':'mg',    
        'grams':'g',  
        'kilograms':'kg', 
        'nanoLiter':'ng', 
        'microLiter':'ul',    
        'microliter':'ul',    
        'milliLiter':'ml',    
        'Liters':'L',
        'nanoMolar':'nM', 
        'microMolar':'uM',    
        'milliMolar':'mM',    
        'Molar':'M',
        'nanomole':'nm', 
        'micromole':'um',    
        'millimole':'mm',    
        'mole':'m',
        'nanograms/microLiter': 'ng/ul',
        'Units/microliter': 'U/ul',
        'Units': 'U',
        # 'X':'X',
        'minutes':'min', 
        'minute':'min', 
        'mins':'min', 
        'minu':'min', 
        'seconds':'sec',    
        'second':'sec',    
        'sec':'sec',    
        'hour':'hr',    
        'hours':'hr',    
        'day':'d',  
        'days':'d',  
        'degrees Celsius':'C', 
        'celsius':'C', 
        'farenheit':'F', 
        'kelvin':'K', 
        }

    try:
        short_units = d[units]
    except KeyError:
        short_units = units

    return short_units


def labeler(object_dict):
    output = {}
    
    if object_dict['verb'] in MANUAL_VERBS:
        verb_attrib_order = list(MANUAL_LAYER[object_dict['verb']]) # if this is not deep copied, the pop(settify) messes it up
        output['display_order'] = verb_attrib_order
        
        for item in verb_attrib_order:
            if 'name' in object_dict.keys():
                output['name'] = object_dict['name']
            if item in object_dict.keys():
                output[item] = object_dict[item]
            if 'duration' in object_dict.keys() and 'duration_units' in object_dict.keys():
                output['time'] = [object_dict['duration'], object_dict['duration_units']]    
            if 'duration' in object_dict.keys() and 'duration_units' not in object_dict.keys():
                output['time'] = [object_dict['duration'], 'sec']   
            if 'settify' in item:
                output.update(settify(object_dict, summary=True))    

            #SPECIAL CASES:
            if 'call-for-protocol' in object_dict['verb']:
                output['protocol_link'] = object_dict['protocol_name']    

        if 'settify' in verb_attrib_order:
            
            settify_order = ['temp', 'speed', 'conc', 'vol', 'mass', 'time', 'technique_comment', 'link']
            [output['display_order'].append(r) for r in settify_order if r in output.keys()]
            output['display_order'].pop(output['display_order'].index('settify'))
        
    return output 
        
def get_timeunit(time_var, desired_unit = 'sec'):
    ''' time_var = [value_str, 'units']
    return (float(min_value), [,float(max_value)], 'units', 'original units')
    '''
    factor = {
        'sec' : {'sec': 1, 'min': 60, 'hrs': 3600,'h': 3600, 'd' : 86400, 'yrs':  31536000},
        'min' : {'sec': 1/60, 'min': 1, 'hrs': 60, 'h': 60,'d' : 1440, 'yrs':  525600},
        'hrs' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'h' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'd' : {'sec': 1/86400, 'min': 1/3600, 'hrs': 1/60, 'h': 1/60, 'd' : 1, 'yrs':  365},
        'yrs' : {'sec': 1/31536000, 'min': 1/525600, 'hrs': 1/8760, 'h': 1/8760, 'd' : 1/365, 'yrs':  1},
        }
    if isinstance(time_var[0], str) and '-' in time_var[0]:    

        min_time = str(time_var[0][:time_var[0].index('-')])
        max_time = str(time_var[0][time_var[0].index('-')+1:])

        return ((float(factor[desired_unit][time_var[1]]) * float(min_time)), 
                (float(factor[desired_unit][time_var[1]]) * float(max_time)), 
                desired_unit, 
                time_var[1])
    else:
        return ((float(factor[desired_unit][time_var[1]]) * float(time_var[0])),
                desired_unit, 
                time_var[1])

def eval_time(node, value = 'min_time'):
    ''' time_var = [value_str, 'units']
    return (float(min_value), [,float(max_value)], 'units', 'original units')
    '''

    # action_min_time = 0
    # action_max_time = 0
    time_unit = 'sec'

    factor = {
        'sec' : {'sec': 1, 'min': 60, 'hrs': 3600,'h': 3600, 'd' : 86400, 'yrs':  31536000},
        'min' : {'sec': 1/60, 'min': 1, 'hrs': 60, 'h': 60,'d' : 1440, 'yrs':  525600},
        'hrs' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'h' : {'sec': 1/3600, 'min': 1/60, 'hrs': 1, 'h': 1, 'd' : 24, 'yrs':  8760},
        'd' : {'sec': 1/86400, 'min': 1/3600, 'hrs': 1/60, 'h': 1/60, 'd' : 1, 'yrs':  365},
        'yrs' : {'sec': 1/31536000, 'min': 1/525600, 'hrs': 1/8760, 'h': 1/8760, 'd' : 1/365, 'yrs':  1},
        }
    
    if 'time_units' in node and node['time_units'] is not None:
        time_unit = node['time_units']

        if time_unit == "minutes":          # TEMP FIX TO SEE IF THIS WORKS.  SOME PROTOCOLS NEED TO BE CORRECTED.
            time_unit = "min"

    if value in node and node[value] is not None:
        return float(factor['sec'][time_unit]) * float(node[value])

    try: 
        return float(factor['sec'][time_unit]) * float(node['min_time'])
    except:
        return 0


class ProtocolChangeLog(object):
    def __init__(self, old_state, new_state):
        self.old_record = old_state
        self.new_record = new_state
        self.old = self.record_to_dict(self.old_record)
        self.new = self.record_to_dict(self.new_record)
        self.hdf  = {}

        if self.old:
            self.diff_protocol_keys()
            self.diff_nodes()
        else:
            self.log_item(self.new_record.pk, 'create', 'protocol', self.new)

    def record_to_dict(self, record):
        result = {}
        if record:
            tmp_dict = record.__dict__

            for key in tmp_dict:
                if key[0] != "_":
                    result[key] = tmp_dict[key]

        return result

    def log_item(self, objectid, event, otype, data, parent_id=None):
        new = True

        if not event in self.hdf:
            self.hdf[event] = []

        # CHECK TO SEE IF THIS ITEM IS ALREADY IN THE LOG OR NOT
        for item in self.hdf[event]:
            if item['id'] == objectid and item['type'] == otype:   # THEY ARE THE SAME OBJECT
                item['attrs'].update( data )
                new = False

        if new:
            self.hdf[event].append( { 'id':objectid, 'type':otype, 'attrs':data, 'parent_id':parent_id } )

    def diff_protocol_keys(self):
        ''' 
        Takes the two Protocol Model Objects and diff's their attributes except for the JSON (data) & date fields.
        '''
        d = DataDiffer(self.old, self.new)
        changed = d.changed()

        if 'name' in changed: 
            self.log_item(objectid = self.old['id'], event='update', otype="protocol", data = { "name": self.new['name']} )        

        if 'id' in changed and 'author_id' not in changed:
            self.log_item(objectid = self.old['id'], event = 'clone', otype="protocol", data = { "pk": self.new['id']} )
            self.log_item(objectid = self.new['id'], event = 'create', otype="protocol", data = { "pk": self.new['data']} )

        if 'user' in changed:
            self.log_item(objectid = self.new['id'], event = 'forked', otype="protocol", data = { "author": self.new['author'] })
            # self.log_item(objectid = self.new['id'], event = 'update', data = { "author": self.new.author })

        if "published" in changed and 'id' not in changed:
            self.log_item(objectid = self.old['id'], event = 'update', otype="protocol", data = { "published": self.new['published'] })

        if "public" in changed:
            self.log_item(objectid = self.old['id'], event = 'update', otype="protocol", data = { "public": self.new['public'] })    

        if "description" in changed:
            self.log_item(objectid = self.old['id'], event = 'update', otype="protocol", data = { "description": self.new['description'] }) 

    # def diff_dict(self, objid=None):
    #     '''this method takes a dict and finds the differences in it catching the following diffs:
    #         key-value pairs: 
    #         triggered by a unicode / int / float / str type. 
    #         finds the added, removed, changed key value pairs and creates a log for each change
            
    #         list objects:
    #         triggered by list type. calls the diff_list method
    #     '''

    #     if not objid: # if dict is protocol.data:
    #         obj_old = self.old.data
    #         obj_new = self.new.data
    #         # print "diffing data_a and data_b"
        
    #     else: # all other dicts in protocol.nodes
    #         obj_old = self.old.nodes[objid]
    #         obj_new = self.new.nodes[objid] 
    #         # print "diffing %s, %s "% (obj_old['name'], obj_new['name'])
        
    #     diff = DataDiffer(obj_old, obj_new) ## diff the step content
    #     # print "added: %s, \n deleted: %s,  \n update: %s"% (diff.added(), diff.removed(), diff.changed())

    #     all_keys = set(obj_old.keys()).union(set(obj_new.keys()))

    #     for key in all_keys:
    #         if key in diff.changed():
    #             if isinstance(obj_old[key], list):       
    #                 self.diff_list(obj_old[key], obj_new[key])
    #                 # print "unpacking lisf of %s and %s"% (type(obj_old), type(obj_new))

    #             if isinstance(obj_old[key], (int, float, unicode, str)):
    #                 self.log_item(objectid = objid, event = "update", data = {key: obj_new[key]})
    #                 # print "logged changed %s, %s "% (objid, obj_new[key])
                
    #         if key in diff.added():
    #             self.log_item(objectid = objid, event = "create", data = { key: obj_new[key]} )
    #             # print "logged add %s, %s "% (objid, obj_new[key])
            
    #         if key in diff.removed():
    #             self.log_item(objectid = objid, event = "delete", data = { key: obj_old[key]} )                
    #             # print "logged remove%s, %s "% (objid, obj_new[key])

    def diff_nodes(self):
        '''
        Diff's nodes that are attached to protocols.
        '''

        old_ids = self.old_record.nodes.keys()
        new_ids = self.new_record.nodes.keys()

        for key in old_ids:     # UPDATED AN DELETED NODES
            if key in new_ids:  # CHECK FOR NODE EDIT
                # print "\nNODE EDIT: %s" % key
                new_node = self.new_record.nodes[key]
                node_type = new_node.__class__.__name__.lower()

                changes = self.node_changes(self.clean_node_data(self.old_record.nodes[key]), self.clean_node_data(new_node))

                for edit_type in ['create', 'update', 'delete']:
                    if changes[edit_type]:
                        self.log_item(key, edit_type, node_type, changes[edit_type], parent_id=new_node.parent.id )

                new_ids.remove(key)
            else:
                node = self.old_record.nodes[key]
                self.log_item(key, "delete", node.__class__.__name__.lower(), self.clean_node_data(node), parent_id=node.parent.id )

        for key in new_ids:     # NEW NODES
            node = self.new_record.nodes[key]
            self.log_item(key, "create", node.__class__.__name__.lower(), self.clean_node_data(node), parent_id=node.parent.id )

    def clean_node_data(self, node):
        '''
        Returns a Node in the cleaned up format for logging
        '''
        result = {}

        for key, item in node.items():
            if key not in ['steps', 'actions', 'machine', 'components', 'thermocycler']:
                result[key] = node[key]

        return result

    def node_changes(self, old_node, new_node):
        result = { 'create':{}, 'update':{}, 'delete':{} }
        differ = DataDiffer(old_node, new_node)

        for key in differ.changed():
            result['update'][key] = new_node[key]

        for key in differ.added():
            result['create'][key] = new_node[key]

        for key in differ.removed():
            result['delete'][key] = new_node[key]

        return result


    # def diff_list(self, list_a, list_b):         
    #     ''' this method takes a list of object ids and compares it between the old and the new list. 
    #         it will catch a few events: 
    #         1. turns the list of objects into a dict of objectids for ease of compare
    #         2. finds the added removed or edited objects in each list
    #         3. for added or removed objects it triggers a log event
    #         4. for changed objects it recurses to diff_dict'''

    #     print "DIFF LIST CALLED"

    #     old_list = dict((item['objectid'],item) for item in list_a)
    #     new_list = dict((item['objectid'],item) for item in list_b)
        
    #     # find changes between list objects (add, delete update)        
    #     diff_list_items = DataDiffer(old_list, new_list)
    #     changed = diff_list_items.changed()
    #     added = diff_list_items.added()
    #     removed = diff_list_items.removed()
    #     # print "added: %s, \n deleted: %s,  \n update: %s"% (diff_list_items.added(), diff_list_items.removed(), diff_list_items.changed()) 
        
    #     ### Place Holder for finding chaned Order in list ###

    #     all_objectids = set(old_list.keys()).union(set(new_list.keys()))
    #     for objid in all_objectids:
    #         if objid in added: 
    #             self.log_item(objectid = objid, event = 'create', otype="step", data = self.new_record.nodes[objid])
    #             # print "logged add%s, %s "% (objid, self.new.nodes[objid])

    #         if objid in removed:
    #             self.log_item(objectid = objid, event = 'delete', otype="", data = self.old_record.nodes[objid])
    #             # print "logged remove%s, %s "% (objid, self.old.nodes[objid])
            
    #         if objid in changed: 
    #            self.diff_dict(objid) # recursive call. 
    #            # print 'recursing dict %s' %objid 

class DataDiffer(object):    

    def __init__(self, old_data, new_data, **kwargs):
        self.old_data, self.new_data = old_data, new_data
        self.set_a, self.set_b = set(old_data.keys()), set(new_data.keys())
        self.intersect = self.set_a.intersection(self.set_b)
    def removed(self):
        return list(self.set_a - self.intersect)
    def added(self):
        return list(self.set_b - self.intersect)
    def changed(self, **kwargs):
        delta = list(o for o in self.intersect if self.new_data[o] != self.old_data[o])
        return delta
    def unchanged(self):
        return list(o for o in self.intersect if self.new_data[o] == self.old_data[o])
