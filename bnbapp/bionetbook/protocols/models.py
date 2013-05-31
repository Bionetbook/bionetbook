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
# from protocols.helpers import settify, unify
# from protocols.settify import settify
# from protocols.utils import VERB_FORM_DICT
from protocols.utils import MACHINE_VERBS, COMPONENT_VERBS, THERMOCYCLER_VERBS, MANUAL_LAYER, MANUAL_VERBS, settify, labeler 

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
        
        new_slug = self.generate_slug()

        if not new_slug == self.slug:
            self.slug = new_slug
            #self.slug = self.generate_slug()
            #self.save()
            super(Protocol, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.

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
        #try:
        #    Protocol.objects.get(slug=slug)
        #    return "%s-%d" % (slug, self.pk)
        #except ObjectDoesNotExist:
        #    return slug
        if self.pk:
            return "%d-%s" % (self.pk, slug)
        else:
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

                for key in ['thermocycle', 'components']:
                    if key in action:
                        for item in action[key]:
                            result[item['objectid']] = item

                if 'machine' in action:
                    result[action['machine']['objectid']] = action['machine']
                            
        return result

    
    def get_machines(self):
         return [r for r in self.get_actions() if self.nodes[r].has_machine()]
    
    def get_actions(self):
        return [r[2] for r in self.get_action_tree('objectid')]    

    
    def get_steps(self):
        return [r['objectid'] for r in self.steps]

    
    def get_components(self):
        return [r for r in self.get_actions() if self.nodes[r].has_components()]

    def get_thermocycle(self):
        return [r for r in self.get_actions() if self.nodes[r].has_thermocycler()]    
 
    def get_manual(self):
        return [self.nodes[r]['objectid'] for r in self.get_actions() if self.nodes[r].has_manual()]    

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

    def update_duration(self):
        pass

    def action_children_json(self):
        out = []
        for action in self.get_actions():
            children = self.nodes[action].children
            if children:
                temp = []
                for child in children:
                    temp.append(child['objectid'])
                
                out.append({action: temp})
                
            else: 
                out.append({action: None})
        return out


    def protocol_tree_json(self):
        out = []
        for step in self.get_steps():
            step_dict={}
            step_dict[step] = []
            actions = [r['objectid'] for r in self.nodes[step].children] 
            for action in actions:
                action_dict = {}
                children = self.nodes[action].children
                if children:
                    action_dict[action] = [r['objectid'] for r in self.nodes[action].children]
    
                else: 
                    action_dict[action] = None

                step_dict[step].append(action_dict)    
                
            out.append(step_dict)
        return out        


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

    def update_duration(self):
        pass


class Component(NodeBase):

    def __init__(self, protocol, parent=None, data=None, **kwargs):
        #self.parent = parent
        super(Component, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'name' in self and not['name'] and 'reagent_name' in self:
            self['name'] = self.pop("reagent_name")

        if 'components' in parent:
            if parent['components']:
                if self['objectid'] not in [x['objectid'] for x in parent['components']]:
                    parent['components'].append(self)
                return

        parent['components'] = [self] # ANY OTHER CASE, MAKE SURE THIS IS REGISTERED WITH THE PARENT

        
    def get_absolute_url(self):
        return reverse("component_detail", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'component_slug':self.slug  })

    def get_update_url(self):
        return reverse('component_edit', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'component_slug':self.slug  })

    def get_delete_url(self):
        return reverse('component_delete', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'component_slug':self.slug  })

    # @property
    # def title(self):
    #     return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])

    # @property
    # def parent(self):
    #     return self.action

    @property
    def label(self):
        return settify(self, summary = False)

    @property
    def summary(self):
        ''' takes self.label as a list and turns it into a dict:
            u'25 degrees Celsius', u'2 minutes' -> 
            {temp: '25C', time: '2 min'}'''
        
        tmp = settify(self, summary = True)
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

        # if 'machine' in parent:
        #     parent['machine'] = self
        
        parent['machine'] = self # ANY OTHER CASE, MAKE SURE THIS IS REGISTERED WITH THE PARENT


        super(Machine, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        
    def get_absolute_url(self):
        return reverse('machine_detail', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'machine_slug':self.slug  })
        #return reverse("machine_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'machine_slug':self.slug  })

    def get_update_url(self):
        return reverse('machine_edit', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'machine_slug':self.slug  })

    def get_delete_url(self):
        return reverse('machine_delete', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'machine_slug':self.slug  })


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
        tmp = settify(self, shorthand = True, summary = True)
        tmp['name'] = self['name']  

        return tmp   

class Thermocycle(NodeBase):
        
    def __init__(self, protocol, parent=None, data=None, **kwargs):
        #self.parent = parent
        super(Thermocycle, self).__init__(protocol, parent=parent, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        # REGISTER SELF WITH PARENT?

        if 'thermocycle' in parent:
            if parent['thermocycle']:
                if self['objectid'] not in [x['objectid'] for x in parent['thermocycle']]:
                    parent['thermocycle'].append(self)
                return
        
        parent['thermocycle'] = [self] # ANY OTHER CASE, MAKE SURE THIS IS REGISTERED WITH THE PARENT

        # if 'reagent_name' in self:
        #     self['name'] = self.pop("reagent_name")
        
    def get_absolute_url(self):
        return reverse("thermocycle_detail", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'thermocycle_slug':self.slug  })

    def get_update_url(self):
        return reverse('thermocycle_update', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'thermocycle_slug':self.slug  })

    def get_delete_url(self):
        return reverse('thermocycle_delete', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.parent.slug, 'action_slug':self.parent.slug, 'component_slug':self.slug  })

    # def get_absolute_url(self):
    #     return "#NDF"
    #     #return reverse("thermocycle_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'thermocycler_slug':self.slug  })

    # def update_data(self, data={}, **kwargs):
    #     super(Thermocycle, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

    #     if 'phases' in data:
    #         self['phases'] = [ Phase(self.protocol, parent=self, data=a) for a in data['settings'] ]
    #     else:
    #         self['phases'] = []

    @property
    def label(self):
        return settify(self, shorthand = True)

    @property
    def summary(self):
        
        tmp = settify(self, shorthand = True, summary = True)
        tmp['name'] = self['name']          
        return tmp    


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

    def machine_create_url(self):
        return reverse("machine_create", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })
        
    def thermocycle_create_url(self):
        return reverse("thermocycle_create", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })

    def component_create_url(self):
        return reverse("component_create", kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug })

    # def machine_update_url(self):
    #     return reverse('machine_edit', kwargs={'owner_slug':self.protocol.owner.slug, 'protocol_slug': self.protocol.slug, 'step_slug':self.parent.slug, 'action_slug':self.slug, 'machine_slug':self.machine.slug  })    
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
    def summary(self):
        ''' takes self.label as a list and turns it into a dict:
            u'25 degrees Celsius', u'2 minutes' -> 
            {temp: '25C', time: '2 min'}'''

        return labeler(self)


    @property
    def children(self):
        
        if type(self.components) == 'list' or 'machine' in self:
            return [self['machine']]

        if type(self.machine) == 'NoneType' and 'components' in self:   
            return self['components']
        
        if 'components' in self:
            return self['components']

        if 'machine' in self:
            return [self['machine']]

        if 'thermocycle' in self:
            return self['thermocycle']   

        else:
            return None

    def delete_child_node(self, node_id):
        """
        Removes a Child Node with the given name from the list of nodes
        Though it can be called directly it is meant to be called from the protocol and trickle down
        """
        #print "%s (%s): REMOVING -> %s" % (self.__class__.__name__, self['objectid'], node_id)
        print "ACTION DELETE"
        if 'machine' in self:
            print "HAS MACHINE"
            if self['machine']['objectid'] == node_id:
                print "REMOVE MACHINE"
                del( self['machine'] )
                return

        if 'thermocycle' in self and node_id in [r['objectid'] for r in self['thermocycle']]:
            self['thermocycle'] = [ x for x in self['thermocycle'] if x['objectid'] is not node_id ]
            return

        if 'components' in self and node_id in [r['objectid'] for r in self['components']]:
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

    def has_manual(self):
        if 'verb' in self:
            return self['verb'] in MANUAL_VERBS
        return False    

    def update_duration(self):
        pass

    def childtype(self):
        if self['verb'] in COMPONENT_VERBS: 
            return 'components'
        if self['verb'] in MACHINE_VERBS:
            return 'machine'
        if self['verb'] in THERMOCYCLER_VERBS:
            return 'thermocycle'            
        if self['verb'] in MANUAL_VERBS:
            return 'manual'
        else:
            return None


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


    def update_duration(self):
        pass

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
