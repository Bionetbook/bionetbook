import string
import random
import math
import itertools
import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel

from organization.models import Organization
from protocols.helpers import settify, unify
# from protocols.settify import settify
# from protocols.utils import VERB_FORM_DICT
from protocols.utils import MACHINE_VERBS, COMPONENT_VERBS, THERMOCYCLER_VERBS

COMPONENT_KEY = "components"
#MACHINE_VERBS = ['heat', 'chill', 'centrifuge', 'agitate', 'collect', 'cook', 'cool', 'electrophorese', 'incubate', 'shake', 'vortex']

class Protocol(TimeStampedModel):

    # STATUS_DRAFT = "draft"
    # STATUS_PUBLISHED = "published"
    # STATUS = (
    #    (STATUS_DRAFT, _(STATUS_DRAFT)),
    #    (STATUS_PUBLISHED, _(STATUS_PUBLISHED)),
    # )

    parent = models.ForeignKey("self", blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True)
    owner = models.ForeignKey(Organization)
    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    raw = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    note = models.TextField(_("Notes"), blank=True, null=True)
    # protocol_input = models.CharField(_("Input"), max_length=255, unique=True)
    # protocol_output = models.CharField(_("Output"), max_length=255, unique=True)

    published = models.BooleanField(_("Published"), default=False)
    public = models.BooleanField(_("Public"), default=False)
    # status = models.CharField(_("Status"), max_length=30, default=STATUS_DRAFT, choices=STATUS)
    # version = models.CharField(_("Version"), max_length=100, blank=True, null=True)

    # reference fields
    # url = models.URLField(_("URL"), max_length=255, null=True, blank=True)
    # PMID = models.CharField(_("PMID"), max_length=255, null=True, blank=True)
    # DOI = models.CharField(_("DOI"), max_length=255, null=True, blank=True)
    # document_id = models.CharField(_("Document ID"), max_length=255, null=True, blank=True)


    def __init__(self, *args, **kwargs):
        self.data = {}
        super(Protocol, self).__init__(*args, **kwargs)

        if not self.data:
            self.data={'steps':[]}

        self.rebuild_steps()

    def __unicode__(self):
        return self.name

    def clone(self, name=None, owner=None):
        '''Turns the current instance into a clone of the previous.
        This instance still need to be saved to be committed.'''

        # CAPTURE PK VALUE, SET PARENT TO PK
        parentid = self.pk

        # SET PK TO None
        self.pk = None

        if name:
            self.name = self.generate_name(name)
        else:
            self.name = self.generate_name(self.owner.name + " " + self.name)

        self.slug = self.generate_slug()

        self.published = False
        self.private = True

        # NEED TO SET THE ORGANIZATION
        if owner:
            self.owner = owner

        self.parent = Protocol.objects.get(pk=parentid)


    def save(self, *args, **kwargs):

        #self.set_data_ids()
        #self.set_data_slugs()

        
        # !!!this will overwrite the self.data!!!!11111
        #if self.data:       
            # NEED TO RETURN STEPS TO JSON
        #    self.data['steps'] = self.steps

        # if not self.steps_data:
        #     self.steps

        if not self.name:
            if self.data['Name']:
                self.name = self.data['Name']

        super(Protocol, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.
        if not self.slug:
            self.slug = self.generate_slug()
            self.save()

    ##########
    # URLs

    def get_absolute_url(self):
        return reverse("protocol_detail", kwargs={'owner_slug':self.owner.slug, 'protocol_slug': self.slug})

    def protocol_update_url(self):
        return reverse("protocol_update", kwargs={'protocol_slug':self.slug, 'owner_slug':self.owner.slug})

    def step_create_url(self):
        return reverse("step_create", kwargs={'protocol_slug':self.slug, 'owner_slug':self.owner.slug})

    def protocol_publish_url(self):
        return reverse("protocol_publish", kwargs={'protocol_slug':self.slug, 'owner_slug':self.owner.slug})

    def protocol_duplicate_url(self):
        return reverse("protocol_duplicate", kwargs={'protocol_slug':self.slug, 'owner_slug':self.owner.slug})

    def protocol_outline_url(self):
        return reverse("compare_single_layers", kwargs={'protocol_a_slug':self.slug, 'layers':'none'})

    ##########
    # Generators

    def generate_name(self, name, count=0):

        if count:
            new_name = "%s-%d" % (name, count)
        else:
            new_name = "%s" % (name)

        try:
            Protocol.objects.get(name=new_name)
            return self.generate_name(name, count=count + 1)
        except ObjectDoesNotExist:
            return new_name

    def generate_slug(self):
        slug = slugify(self.name)
        try:
            Protocol.objects.get(slug=slug)
            return "%s-%d" % (slug, self.pk)
        except ObjectDoesNotExist:
            return slug

    def get_hash_id(self, size=6, chars=string.ascii_lowercase + string.digits):
        '''Always returns a unique ID in the protocol'''
        uid_list = []
        uid = ''.join(random.choice(chars) for x in range(size))

        for step in self.steps:
            if hasattr(step, 'objectid'):
                if step['objectid']:
                    uid_list.append(step.objectid)

            for action in step['actions']:
                if hasattr(action, 'objectid'):
                    if action['objectid']:
                        uid_list.append(action['objectid'])

                if COMPONENT_KEY in action.keys():        
                    for reagent in action[COMPONENT_KEY]:
                        if 'objectid' in reagent: # hasattr doesn't work here I think because of unicode
                            uid_list.append(reagent['objectid'])


        if uid not in uid_list:
            return uid

        return self.get_hash_id(size, chars)

    def rebuild_steps(self):
        if self.data and 'steps' in self.data:
            self.data['steps'] = [ Step(protocol=self, data=s) for s in self.data['steps'] ]
            #self.steps_data = [ Step(protocol=self, data=s) for s in self.data['steps'] ]

    # def add_step(self, step):
    #     if not step['objectid'] in [ s['objectid'] for s in self.data['steps'] ]:
    #         print "STEP NOT THERE, ADDING"
    #         #print type(step)
    #         print "IS STEP: %s" % isinstance(step, Step)
    #         self.data['steps'].append(step)
    #         self.rebuild_steps()
    #     else:
    #         print "ALREADY THERE"


    def add_node(self, node):
        '''
        Every node needs to register it's self with a protocol here.  If it's a step it get_steps
        added to the list of steps.  It's written this way to handle other types of Nodes being 
        added with special needs.
        '''
        if not node['objectid'] in self.nodes:
            if isinstance(node, Step):              # IF IT IS A STEP GIVE IT THIS EXTRA STEP
                #print "STEP NOT THERE, ADDING"
                self.data['steps'].append(node)
                self.rebuild_steps()
        #     else:
        #         print "NODE NOT THERE, ADDING"
        #         # IN THIS CASE JUST REGISTER IS WITH THE NODE DICTIONARY
        # else:
        #     print "ALREADY THERE"


        # NEED TO ADD ACTIONS TO THE PROTOCOL


    ###########
    # Validators

    # def has_changed(self, field):
    #     if not self.pk:
    #         return False
    #     old_value = self.__class__._default_manager.filter(pk=self.pk).values(field).get()[field]
    #     return not getattr(self, field) == old_value
  
    ###########
    # Properties

    @property
    def title(self):
        return self.name


    # NEED TO CREATE add AND delete METHODS FOR THE PROPERTY
    @property
    def steps(self):
        # if not self.steps_data:
        #     self.rebuild_steps()
        #     self.steps_data = self.data['steps']

        # return self.steps_data
        return self.data['steps']


    @property
    def status(self):
        if self.public:
            prefix = "Public - "
        else:
            prefix = "Private - "

        if self.published:
            return prefix + "Published"
        else:
            return prefix + "Draft"

    # NEED TO CREATE add AND delete METHODS FOR THE PROPERTY
    @property
    def nodes(self):
        ''' Returns a dictionary containing the '''
        result = {}
        for step in self.steps:
            result[step['objectid']] = step

            for action in step['actions']:
                result[action['objectid']] = action

                for key in ['thermocycle', 'component']:
                    if key in action:
                        for item in action[key]:
                            result[item['objectid']] = item

                if 'machine' in action:
                    result[action['machine']['objectid']] = action['machine']
                            
        return result

    @property
    def get_machines(self):
         return [self.nodes[r]['objectid'] for r in self.get_actions if 'machine' in self.nodes[r].keys() ]

    @property
    def get_actions(self):
        return [r[2] for r in self.get_action_tree('objectid')]    

    @property
    def get_steps(self):
        return [r['objectid'] for r in self.steps]

    @property
    def get_components(self):
        return self.get_reagents_by_action('objectid')
 
    ###########
    # delete node properties:

    def delete_node(self, node_id):
        """ This will remove a child node form a hierarchy """
        node = self.nodes[node_id]
        #print node.__class__.__str__
        parent = node.parent
        parent.delete_child_node(node_id)
        #self.save()

    def delete_child_node(self, node_id):
        """ Removes a Child Node with the given name from the list of nodes """
        #print "%s (%s): REMOVING -> %s" % (self.__class__, self.pk, node_id)
        self.data['steps'] = [ x for x in self.data['steps'] if not x['objectid'] == node_id ]

    # def levels()

    ###########
    # Methods
    @property 
    def get_num_steps(self):
        return len(self.steps)
    
    def get_num_actions(self):
        return [len(s['actions']) for s in self.steps]

    def get_actions_by_step(self):
        actions_by_step = []
        # num_actions = self.get_num_actions()
        for stepnum in range(0, self.get_num_steps):
            tmp = [self.data['steps'][stepnum]['actions'][r]['verb'] for r in range(0, self.get_num_actions()[stepnum])]
            actions_by_step.append(tmp)
        return actions_by_step

    def get_action_tree(self, display = None):
        action_tree = []
        for stepnum in range(0, self.get_num_steps): # traversign all steps
            for actionnum in range(0, len(self.steps[stepnum]['actions'])): # traversing all actions per step
                if display == 'objectid':
                    action_tree.append([stepnum, actionnum, self.steps[stepnum]['actions'][actionnum]['objectid']])
                else:    
                    action_tree.append([stepnum, actionnum, self.steps[stepnum]['actions'][actionnum]['verb']])
        
        return action_tree

    def get_objectid(self, stepnum, actionnum):
        step = self.steps[stepnum]['objectid']
        action = self.steps[stepnum]['actions'][actionnum]['objectid']
        return (step,action)

    def get_reagent_data(self, display=None):
        # function takes the display argument and returns the (step, action) display of the reagent, i.e. verb, objectid, slug etc.  
        ''' this combiones a find technique with a return technique:
        find = self.data['components-location']
        return = through the self.steps accessor and not theough an objid accessor. 


        '''
        self.needed_reagents = []
        
        if self.data['components-location'][0] > 0:  # check if there are components in the protocol:
            for l in self.data['components-location']: # iterate over all step,action locations where there are components
                components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY]) 
                for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['name']
                    objectid = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['objectid']
                    cur_reagent_name = []
                    cur_reagent_name.append(reagent_name)
                    if 'total volume' in reagent_name.lower():
                        continue
                    if display == 'detail':
                        cur_reagent_name.append(l[1])
                        cur_reagent_name.append(l[2])
                    if display == 'all': 
                        tmp = []
                        tmp.append(l[1])
                        tmp.append(l[2])
                        tmp.append(self.steps[l[1]]['actions'][l[2]]['verb'])
                        cur_reagent_name.append(tmp)
                    if display =='name_objectid':
                        cur_reagent_name = (reagent_name, objectid)
                    if display == 'objectid':
                        actionid = self.get_objectid(l[1], l[2])
                        cur_reagent_name = (objectid, actionid[1])
                            
                    self.needed_reagents.append(cur_reagent_name)    

        return self.needed_reagents   

    def get_reagents_by_action(self, out_label='objectid'):
        ''' this combiones a find technique with a return technique:
        find = self.data['components-location']
        return = through the self.steps accessor and not theough an objid accessor. 


        '''
        self.verb_reagents = {}
        for l in self.data['components-location']: # iterate over all step,action locations where there are components 
            components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY]) # iterate over reagents
            verb = self.steps[l[1]]['actions'][l[2]]['verb']
            verbid = self.steps[l[1]]['actions'][l[2]]['objectid']
            if out_label == 'literal':
                self.verb_reagents[verbid]=[]
            if out_label == 'objectid':
                self.verb_reagents[verbid]=[]

            for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['name']
                    if 'total volume' in reagent_name.lower():
                        continue

                    objectid = self.steps[l[1]]['actions'][l[2]][COMPONENT_KEY][r]['objectid']
                    if out_label == 'literal':
                        self.verb_reagents[verbid].append(reagent_name)
                    if out_label == 'objectid':
                        self.verb_reagents[verbid].append(objectid)
        
        return self.verb_reagents  


class NodeBase(dict):
    """Base class for the protocol components"""

    # keylist = ['name','objectid']   # <- REQUIRED OBJECTS FOR ALL NODES

    # ADD _meta CLASS TO USE SOME EXTRA DB-LIKE FUNCTIONALITY
    default_attrs = ['name', 'objectid']

    class Meta:
        def __init__(self, node):
            self.node = node

        def get_all_field_names(self):
            result = self.node.keys()   #[x for x in self.node.keys() if x not in ['components', 'machine', 'termocycler'] ]
            result.sort()
            return result

    def __init__(self, protocol, parent=None, data={}, **kwargs):
        super(NodeBase, self).__init__(**kwargs)
        
        self.protocol = protocol
        if parent:
            self.parent = parent
        else:
            self.parent = self.protocol

        data = self.clean_data(data)

        self._meta = NodeBase.Meta(self)

        # for item in self.keylist:       # REQUIRED ATTRIBUTES
        #     self[item] = None

        self.update_data(data)
        # self.set_defaults()

    def clean_data(self, data):
        # OBJECT KEY GENERATOR IF MISSING
        # if not self['objectid']:
        #    self['objectid'] = self.protocol.get_hash_id()
        if data == None:
            data = {}

        if not 'objectid' in data or not data['objectid']:
            data['objectid'] = self.protocol.get_hash_id()

        if not 'name' in data or not data['name']:
            data['name'] = data['objectid']

        if not 'slug' in data or not data['slug']:
            data['slug'] = slugify(data['objectid'])

        return data

    @property
    def pk(self):
        return "%d-%s" % (self.protocol.pk, self['objectid'])

    @property
    def slug(self):
        #if not self['slug']:
        #    self['slug'] = slugify(self['name'])
        return self['slug']

    @property
    def graph_label(self):
        return self['name']

    def update_data(self, data={}, **kwargs):
        if data:
            for key in data:
                self[key] = data[key]

            if not 'name' in self or not self['name']:
                self['name'] = self['slug']

    def __unicode__(self):
        return self['slug']

    @property
    def title(self):
        if self.parent:
            return "%s - %s" % (self.parent.title, self['name'])
        else:
            return "%s - %s" % (self.protocol.name, self['name'])

    # @property
    # def parent(self):
    #     return self.protocol

    def delete_child_node(self, node_id):
        """ Removes a Child Node with the given name from the list of nodes """
        print "NOT YET IMPLETMENTED FOR %s (%s): REMOVING -> %s" % (self.__class__, self['objectid'], node_id)

    @property    
    def children(self):
        print 'object does not have children'    



class Component(NodeBase):

    def __init__(self, protocol, parent=None, data=None, **kwargs):
        #self.parent = parent
        super(Component, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'reagent_name' in self:
            self['name'] = self.pop("reagent_name")
        
    def get_absolute_url(self):
        return reverse("component_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.parent.step.slug, 'action_slug':self.parent.slug, 'component_slug':self.slug  })

    # @property
    # def title(self):
    #     return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])

    # @property
    # def parent(self):
    #     return self.action

    @property
    def label(self):
        return unify(self, summary = False)

    @property
    def summary(self):
        ''' takes self.label as a list and turns it into a dict:
            u'25 degrees Celsius', u'2 minutes' -> 
            {temp: '25C', time: '2 min'}'''
        
        tmp = unify(self, summary = True)
        tmp['name'] = self['name']      

        return tmp


class Machine(NodeBase):

    default_attrs = ['name', 'objectid', 'min_time', 'max_time', 'time_comment', 'time_units', 'min_temp', 'max_temp', 'temp_comment', 'temp_units', 'min_speed', 'max_speed', 'speed_comment', 'speed_units']

    def __init__(self, protocol, parent=None, data=None, **kwargs):
        #self.action = action
        #self.parent = self.action

        # MAKE SURE THESE ATTRIBUTES ARE IN THE MACHINE OBJECT
        for item in self.default_attrs:
            if item not in data:
                data[item] = None

        super(Machine, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        
    def get_absolute_url(self):
        return "#NDF"
        #return reverse("machine_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'machine_slug':self.slug  })

    # @property
    # def title(self):
    #     return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])

    # @property
    # def parent(self):
    #     return self.action

    @property
    def label(self):
        return settify(self, shorthand = True)

    @property
    def summary(self):
        ''' takes self.label as a list and turns it into a dict:
            u'25 degrees Celsius', u'2 minutes' -> 
            {temp: '25C', time: '2 min'}'''
        output = {}
        
        for i in self.label:
            if 'Celsius' in i or 'degre' in i:
                output['temp'] = str(re.findall(r'\d+',i)[0]) + 'C'
            if 'minute' in i or 'second' in i or 'hour' in i:
                output['time'] = str(re.findall(r'\d+',i)[0]) + str(re.findall(r'\D+',i)[0])

        return output   


class Subphase(NodeBase):

    default_attrs = ['name', 'objectid', 'time', 'temperature']

    def get_absolute_url(self):
        return "#NDF"


class Phase(NodeBase):

    default_attrs = ['name', 'objectid', 'cycles', 'before', 'after']

    def get_absolute_url(self):
        return "#NDF"

    def update_data(self, data={}, **kwargs):
        super(Phase, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'subphases' in data:
            self['subphases'] = [ Subphase(self.protocol, parent=self, data=a) for a in data['subphases'] ]
        else:
            self['subphases'] = []


class Thermocycle(NodeBase):
        
    def get_absolute_url(self):
        return "#NDF"
        #return reverse("thermocycle_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'thermocycler_slug':self.slug  })

    def update_data(self, data={}, **kwargs):
        super(Thermocycle, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'phases' in data:
            self['phases'] = [ Phase(self.protocol, parent=self, data=a) for a in data['phases'] ]
        else:
            self['phases'] = []

    @property
    def label(self):
        return settify(self, shorthand = True)

    @property
    def summary(self):
        ''' finds brothers by: self.parent.children and returns a dict with all the pcr stages :
        
            {'Initial denaturation':
                [
                annealing: {temp = '98C', tmie = 30 seconds}
                ], 
                cycles : '1', before: 'kffgk', after'frrff'}    
            {'Elongation': 
                [
                {'Denaturation': {'98 deg celsius', '30 seconds'}},     
                {'Annealing': {'98 deg celsius', '30 seconds'}},    
                {'extenssion': {'98 deg celsius', '30 seconds'}
                ], 
                cycles: '15', before: 'rrfffr', 'after': 'gffgg'},    
            {'Termination': 
                [
                {'termination'{98 deg celsius', '30 seconds'},
                ],
                cycles: '1', before: 'rfrffr', 'after': 'gerrrg'}, }    

            '''
        output = {}
        tmp_output = {}
        output['name'] = self['name']
        output['phases'] = []
        output['cycles'] = self['cycles']
        parent = self.parent['objectid']

        thermo_ids = [r['objectid'] for r in self.protocol.nodes[parent].children]
        current = thermo_ids.index(self['objectid'])
        
        if current == 0 and len(thermo_ids) == 1:
            output['previous_substep'] = ''
            output['next_substep'] = ''

        if current == 0 and len(thermo_ids) >1:
            output['previous_substep'] = ''
            output['next_substep'] = thermo_ids[1]

        if current > 0 and current < len(thermo_ids) -1 :
            output['previous_substep'] = thermo_ids[current - 1]
            output['next_substep'] = thermo_ids[current + 1]

        if current == len(thermo_ids):
            output['previous_substep'] = thermo_ids[current-1]
            output['next_substep'] = ''

        # for i in thermo_ids:
        #     output['cycles'][self.protocol.nodes[i]['name']] = self.protocol.nodes[i]['cycles'] 
        for j in self['settings']:
            tmp_output[j['name']] = settify(j)
            stage = {}
            stage[j['name']] = {}
            for ii in tmp_output[j['name']]:     
                if 'Celsius' in ii or 'degre' in ii:
                    stage[j['name']]['temp'] = str(re.findall(r'\d+',ii)[0]) + 'C'
                if 'minute' in ii or 'second' in ii or 'hour' in ii:
                    stage[j['name']]['time'] = str(ii) #str(re.findall(r'\d+',ii)[0]) + str(re.findall(r'\D+',ii)[0])

            output['phases'].append(stage)        

        return output           
    


class Action(NodeBase):

    # def __init__(self, protocol, parent=None, data=None, **kwargs):
    #     #self.step = step
    #     self.parent = parent
    #     super(Action, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.            
    
    def update_data(self, data={}, **kwargs):
        super(Action, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'component - list' in data:                                  # rename "componet - list" to "components"
            data['components'] = data.pop("component - list")

        if 'components' in data:                                        # Convert dictionaries into Component Objects
            self['components'] = [ Component(self.protocol, parent=self, data=c) for c in data['components'] ]

        if 'thermocycle' in data:                                        # Convert dictionaries into Thermocycle Objects
            self['thermocycle'] = [ Thermocycle(self.protocol, parent=self, data=c) for c in data['thermocycle'] ] 

        if 'machine' in data and 'verb' in data and data['verb'] in MACHINE_VERBS:            # Make sure this action is supposed to have a "machine" attribute
            self['machine'] = Machine(self.protocol, parent=self, data=data['machine'])

        if not self['name']:                                            # Action default name should be the same as the verb
            self['name'] = self['verb']

        if self['name'] == self['objectid']:        # CORRECT THIS DATA
            self['name'] = self['verb']

        if not self['objectid'] in self.protocol.nodes:
            print "NOT THERE"

        # if 'actions' in self.parent:
        #     self.parent['actions'].append(self)
        # else:
        #     self.parent['actions'] = [self]


    def get_absolute_url(self):
        return reverse("action_detail", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })

    def action_update_url(self):
        return reverse("action_update", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })

    def action_delete_url(self):
        return reverse("action_delete", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })

    # @property
    # def title(self):
    #     return "%s - %s - %s" % (self.protocol.name, self.step['name'], self['name'])

    # @property
    # def parent(self):
    #     return self.step

    @property
    def components(self):
        if 'components' in self:
            return self['components']
        else:
            return None

    @property
    def machine(self):
        if 'machine' in self:
            return self['machine']
        else:
            return None

    @machine.setter
    def machine(self, value):
        if value.__class__ == Machine:
            self['machine'] = value
        else:
            raise ValueError("Action's machine attribute can only accept a Machine object")        

    @property
    def thermocycle(self):
        if 'thermocycle' in self:
            return self['thermocycle']
        else:
            return None


    @property
    def children(self):
        
        if type(self.components) == 'list' or 'machine' in self:
            return self['machine']

        if type(self.machine) == 'NoneType' and 'components' in self:   
            return self['components']
        
        if 'components' in self:
            return self['components']

        if 'machine' in self:
            return self['machine']

        if 'thermocycle' in self:
            return self['thermocycle']   

        else:
            return None

    def delete_child_node(self, node_id):
        """
        Removes a Child Node with the given name from the list of nodes
        Though it can be called directly it is meant to be called from the protocol and trickle down
        """
        #print "%s (%s): REMOVING -> %s" % (self.__class__, self['objectid'], node_id)
        if self['machine']['objectid'] == node_id:
            del( self['machine'] )
        if node_id in [r['objectid'] for r in self['thermocycle']]:
            self['thermocycle'] = [ x for x in self['thermocycle'] if x['objectid'] is not node_id ]
        else:
            self['components'] = [ x for x in self['components'] if x['objectid'] is not node_id ]

    def has_components(self):
        if 'verb' in self:
            return self['verb'] in COMPONENT_VERBS
        return False

    def has_machine(self):
        if 'verb' in self:
            return self['verb'] in MACHINE_VERBS
        return False

    def has_thermocycler(self):
        if 'verb' in self:
            return self['verb'] in THERMOCYCLER_VERBS
        return False


class Step(NodeBase):

    # def __init__(self, protocol, parent=None, data=None, **kwargs):
    #     super(Step, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

    def update_data(self, data={}, **kwargs):
        super(Step, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'actions' in data:
            self['actions'] = [ Action(self.protocol, parent=self, data=a) for a in data['actions'] ]
        else:
            self['actions'] = []

        # UPDATE DURATION AT THE SAME TIME
        duration = 0
        for action in self['actions']:
            if 'duration' in action:
                duration += int(action['duration'])

        # self['duration'] = duration


        #print self.protocol.nodes

        # if not data['objectid'] in self.protocol.nodes:
        #     print "STEP NOT THERE, ADDING"
        self.protocol.add_node(self)
        # else:
        #     print "ALREADY THERE"

    def get_absolute_url(self):
        return reverse("step_detail", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    def step_update_url(self):
        return reverse("step_update", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    def add_action_url(self):
        return reverse("action_create", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    def action_verb_list_url(self):
        return reverse("action_verb_list", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    def step_delete_url(self):
        return reverse("step_delete", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    # @property
    # def title(self):
    #     return "%s - %s" % (self.protocol.name, self['name'])

    def delete_child_node(self, node_id):
        """
        Removes a Child Node with the given name from the list of nodes
        Though it can be called directly it is meant to be called from the protocol and trickle down
        """
        #print "%s (%s): REMOVING -> %s" % (self.__class__, self['objectid'], node_id)
        self['actions'] = [ x for x in self['actions'] if not x['objectid'] == node_id ]


    @property
    def actions(self):
        if 'actions' in self:
            return self['actions']
        else:
            return None 

    @property
    def children(self):
        if 'actions' in self:
            return self['actions']
        else:
            return None

    # NEED TO UPDATE URLS TO USE THE BELOW METHOD
    # def __getitem__(self, key):
    #     val = dict.__getitem__(self, key)

    #     if key == "slug":
    #         val = slugify(dict.__getitem__(self, 'name'))

    #     return val


    #def get_hash_id(self, size=6, chars=string.ascii_lowercase + string.digits):
    #    '''Always returns a unique ID in the protocol'''
    #    uid_list = []
    #    uid = ''.join(random.choice(chars) for x in range(size))
    #    return uid
    # @property
    # def actions(self):
    #     return 



# class ProtocolIngest(Protocol):
#     '''Used for loading protocols from JSON formatted text files.'''

#     class Meta:
#         db_table = 'protocols_protocol'

#     def read_data(self, *args):
#         filename = str(args[0])
#         self.data = open(filename, 'r').read()
#         if self.data:
#             return self.data
#         else:
#             print 'no data loaded'




