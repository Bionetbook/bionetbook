import string
import random
import math
import itertools

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import django.utils.simplejson as json
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel

from organization.models import Organization
from protocols.utils import settify , unify
# from protocols.utils import VERB_FORM_DICT

COMPONENT_KEY = "components"

class Protocol(TimeStampedModel):

    # STATUS_DRAFT = "draft"
    # STATUS_PUBLISHED = "published"
    # STATUS = (
    #    (STATUS_DRAFT, _(STATUS_DRAFT)),
    #    (STATUS_PUBLISHED, _(STATUS_PUBLISHED)),
    # )

    parent = models.ForeignKey("self", blank=True, null=True)
    #author = models.ForeignKey(User)
    owner = models.ForeignKey(Organization)
    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    raw = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # protocol_input = models.CharField(_("Input"), max_length=255, unique=True)
    # protocol_output = models.CharField(_("Output"), max_length=255, unique=True)

    published = models.BooleanField(_("Published"), default=False)
    public = models.BooleanField(_("Published"), default=False)
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
            self.data={}

        self.rebuild_steps()



    def __unicode__(self):
        return self.name

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
    # Generators

    def generate_slug(self):
        slug = slugify(self.name)
        try:
            Protocol.objects.get(slug=slug)
            return "%s-%d" % (slug, self.pk)
        except ObjectDoesNotExist:
            return slug

    def get_absolute_url(self):
        return reverse("protocol_detail", kwargs={'protocol_slug': self.slug})

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

    ###########
    # Validators

    # def set_data_ids(self):
    #     for step in self.steps:
    #         if not step['objectid']:
    #             step['objectid'] = self.get_hash_id()

    #         for action in step['actions']:
    #             if not action['objectid']:
    #                 action['objectid'] = self.get_hash_id()
                
    #             if COMPONENT_KEY in action.keys():
    #                 for reagent in action[COMPONENT_KEY]:
    #                     if 'objectid' not in reagent.keys():
    #                         reagent['objectid'] = self.get_hash_id()

    # def set_data_slugs(self):
    #     for step in self.steps:
    #         if not step['slug']:
    #             step['slug'] = slugify(step['objectid'])

    #         for action in step['actions']:
    #             if 'slug' in action and not action['slug']:
    #                 action['slug'] = slugify(action['objectid'])

    #             if COMPONENT_KEY in action.keys():
    #                 for reagent in action[COMPONENT_KEY]:
    #                     if 'slug' not in reagent.keys():
    #                         reagent['slug'] = slugify(reagent['objectid'])


    ###########
    # Properties


    # NEED TO CREATE add AND delete METHODS FOR THE PROPERTY
    @property
    def steps(self):
        # if not self.steps_data:
        #     self.rebuild_steps()
        #     self.steps_data = self.data['steps']

        # return self.steps_data
        return self.data['steps']


    # NEED TO CREATE add AND delete METHODS FOR THE PROPERTY
    @property
    def nodes(self):
        result = {}
        for step in self.steps:
            result[step['objectid']] = step

            for action in step['actions']:
                result[action['objectid']] = action

                if COMPONENT_KEY in action:
                    for component in action[COMPONENT_KEY]:
                        result[component['objectid']] = component

        return result
    ###########
    # test properties:

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

    def nodes_detail(act):
        # act = [0, 0, u'call_for_protocol'] -> 0-0-call_for_protocol
        return ''.join(str(act)).replace(', ','-').replace('[','').replace(']','').replace('\'','').replace('-u','-')


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

    def objectid2name(self, objid, **kwargs):
    
        ''' function takes in a protocol instance (self) and an objid. If the objid is not in the protocol instance, a False is returned. 
        if the objid is in the protocol it returns a list:
        nodetype = True : step action or reagent
        name = True: returns the name of the object.
        location = True: returns a (step, action) location. If step, it returns a single int.
        
        attributes = True: return list of all attribute names
        units = True: returns a shorthand format for reagent units
        parents = True: returns parents
        
        full_data = True: adds (merges) all key: value pairs from the object to the outDict. object_data overrites 
        not completed:
        siblings = True: returns all siblings
        
        children = True: returns children
        

        ''' 
        # def unify(units_dict, shorthand = True):

        #     units = ''

        #     conc = dict((k, v) for k, v in units_dict.iteritems() if 'conc' in k)
        #     vol = dict((k, v) for k, v in units_dict.iteritems() if 'vol' in k)
        #     mass = dict((k, v) for k, v in units_dict.iteritems() if 'mass' in k)

        #     if conc:
        #         # check that all data is present:
        #         if not conc['conc_units']:
        #             return 'no concentration units specified for %s' % units_dict['name']
        #         if 'max_conc' not in conc and 'min_conc' not in conc:
        #             return 'enter concentration units for %s' % units_dict['name']    

        #         if 'max_conc' in conc and 'min_conc' in conc:

        #             if conc['max_conc'] == conc['min_conc']:
        #                 units = conc['max_conc']
        #             else:
        #                 units = units + conc['min_conc'] + '-' + conc['max_conc']
        #         else:
        #             if 'max_conc' in conc:
        #                  units = conc['max_conc']
        #             if 'min_conc' in conc:
        #                  units = conc['min_conc']                        
                    
        #         units = units + ' ' + conc['conc_units']  

            
        #     if vol:
        #         if not vol['vol_units']:
        #             return 'no Volume units specified for %s' % units_dict['name']
        #         if 'max_vol' not in vol and 'min_vol' not in vol:
        #             return 'enter Volume units for %s' % units_dict['name']

        #         if 'max_vol' in vol and 'min_vol' in vol:

        #             if vol['max_vol'] == vol['min_vol']:
        #                 units = units + ', ' + vol['max_vol']
        #             else:
        #                 units = units + ', ' + vol['min_vol'] + '-' + vol['max_vol']

        #         else:
        #             if 'max_vol' in vol:
        #                  units = vol['max_vol']
        #             if 'min_vol' in vol:
        #                  units = vol['min_vol']          
                
        #         units = units + ' ' + vol['vol_units'] 

        #     if mass:
        #         if not mass['mass_units']:
        #             return 'no mass units specified for %s' % units_dict['name']
        #         if 'max_mass' not in mass and 'min_mass' not in mass:
        #             return 'enter mass units for %s' % units_dict['name']

        #         if 'max_mass' in mass and 'min_mass' in mass:

        #             if mass['min_mass'] == mass['max_mass']:
        #                 units = units + ', ' + mass['max_mass']
        #             else:
        #                 units = units + ', ' + mass['min_mass'] + '-' + mass['max_mass']

        #         else:
        #             if 'max_mass' in mass:
        #                  units = mass['max_mass']
        #             if 'min_mass' in mass:
        #                  units = mass['min_mass']

        #         units = units + ' ' + mass['mass_units']

        #     if shorthand == True:
        #         units = units.replace('nanograms','ng') 
        #         units = units.replace('micrograms','ug')    
        #         units = units.replace('milligrams','mg')    
        #         units = units.replace('grams','g')  
        #         units = units.replace('kilograms','kg') 
        #         units = units.replace('nanoLiter','ng') 
        #         units = units.replace('microLiter','ul')    
        #         units = units.replace('microliter','ul')    
        #         units = units.replace('milliLiter','ml')    
        #         units = units.replace('Liters','L')
        #         units = units.replace('nanoMolar','nM') 
        #         units = units.replace('microMolar','uM')    
        #         units = units.replace('milliMolar','mM')    
        #         units = units.replace('Molar','M')
        #         units = units.replace('nanomole','nm') 
        #         units = units.replace('micromole','um')    
        #         units = units.replace('millimole','mm')    
        #         units = units.replace('mole','m')
        #     return units

        default_setting = {}
        default_setting['objectid'] = objid
        default_setting['nodetype'] =  'None'
        default_setting['name'] = 'None'
        default_setting['location'] = []
        default_setting['full_data'] = False
        outDict = {}
        
        # Merging the 2 dicts together, kwargs overites default settings:
        if kwargs:
            for k, v in itertools.chain(default_setting.iteritems(), kwargs.iteritems()):
                outDict[k] = v 
        else:
            for k, v in default_setting.iteritems():
                outDict[k] = v 


        # make lists of all objectid's:
        steps_by_id = [r['objectid'] for r in self.steps]
        #[self.steps[r]['objectid'] for r in range(self.get_num_steps)]
        
        # actions_by_id = self.get_action_tree('objectid')
        actions_by_id = [i[2] for i in self.get_action_tree('objectid')]

        reagents_by_id = [i[0] for i in self.get_reagent_data('objectid')]

        # find what nodetype of objectid:
        if objid in steps_by_id:
            outDict['nodetype'] = 'step'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = [steps_by_id.index(objid)]
            outDict['object_data']  = self.nodes[objid]
            # outDict['slug'] = 
        
        if objid in actions_by_id:
            outDict['nodetype'] = 'action'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = self.get_action_tree()[actions_by_id.index(objid)][:-1]
            outDict['object_data'] = self.nodes[objid]


        if objid in reagents_by_id:
            outDict['nodetype'] = 'reagent'
            outDict['name'] = self.nodes[objid]['name']
            outDict['location'] = self.get_reagent_data('detail')[reagents_by_id.index(objid)][1:3]
            s = self.get_reagents_by_action()
            for k,v in s.items():
                if objid in v:
                    reagent_order = s[k].index(objid)

            outDict['location'].append(reagent_order)
            outDict['object_data'] = self.nodes[objid]
        

        if kwargs:    
        # Return general requensts:   
            if 'attributes' in kwargs and kwargs['attributes'] == True: 
                outDict['attributes'] = outDict['object_data'].keys()
            
            if 'units' in kwargs and kwargs['units'] == True:
                outDict['label'] = unify(outDict['object_data'])

            if 'children' in kwargs and kwargs['children'] == True:
                if outDict['nodetype'] == 'step':
                    outDict['children'] = [r['objectid'] for r in self.nodes[objid]['actions']]
                if outDict['nodetype'] == 'action':
                    outDict['children'] = [r['objectid'] for r in self.nodes[objid][COMPONENT_KEY]]    
                if outDict['nodetype'] == 'reagent':
                     outDict['children'] = None

            if 'parents' in kwargs and kwargs['parents'] == True:
                tmp = self.get_objectid(outDict['location'][0], outDict['location'][1])
                if outDict['nodetype'] =='step':
                    outDict['parents'] = 'protocol'
                if outDict['nodetype'] == 'action':
                    outDict['parents'] = tmp[0]
                if outDict['nodetype'] == 'reagent':
                    outDict['parents'] = tmp[1]        

            if 'full_data' in kwargs and kwargs['full_data']:
                full_data = outDict.pop('object_data')
                temp = {}
                for k, v in itertools.chain(outDict.iteritems(), full_data.iteritems()):
                    temp[k] = v 
                    
                outDict = temp

        # Returm reagent handlers:    
        # destruct object_data unless specicied in options
        if not outDict['full_data'] == True:
            outDict.pop('object_data')
        
        outDict.pop('full_data')    

        return outDict  


class NodeBase(dict):
    """Base class for the protocol components"""

    keylist = ['name','objectid']   # <- REQUIRED OBJECTS FOR ALL NODES

    # ADD _meta CLASS TO USE SOME EXTRA DB-LIKE FUNCTIONALITY

    class Meta:
        def __init__(self, node):
            self.node = node

        def get_all_field_names(self):
            result = self.node.keys()
            result.sort()
            return result

    def __init__(self, protocol, data={}, **kwargs):
        super(NodeBase, self).__init__(**kwargs)
        
        self.protocol = protocol

        self['objectid'] = None #self.get_hash_id()
        self['slug'] = None

        self._meta = NodeBase.Meta(self)

        for item in self.keylist:       # REQUIRED ATTRIBUTES
            self[item] = None

        self.update_data(data)
        self.set_defaults()

    def set_defaults(self):
        # OBJECT KEY GENERATOR IF MISSING
        if not self['objectid']:
            self['objectid'] = self.protocol.get_hash_id()

        if not self['name']:
            self['name'] = self['objectid']

        if not self['slug']:
            self['slug'] = slugify(self['objectid'])

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
        return self.protocol.name

    @property
    def parent(self):
        return self.protocol


class Component(NodeBase):

    def __init__(self, protocol, action=None, data=None, **kwargs):
        self.action = action
        super(Component, self).__init__(protocol, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'reagent_name' in self:
            self['name'] = self.pop("reagent_name")
        
    def get_absolute_url(self):
        return reverse("component_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'component_slug':self.slug  })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])

    @property
    def parent(self):
        return self.action

    @property
    def label(self):
        return unify(self, shorthand = True)

        # self.units = ''
        # conc = dict((k, v) for k, v in self.iteritems() if 'conc' in k)
        # vol = dict((k, v) for k, v in self.iteritems() if 'vol' in k)
        # mass = dict((k, v) for k, v in self.iteritems() if 'mass' in k)

        # if conc:
        #     # check that all data is present:
        #     if not conc['conc_units']:
        #         return 'no concentration units specified for %s' % self['name']
        #     if 'max_conc' not in conc and 'min_conc' not in conc:
        #         return 'enter concentration units for %s' % self['name']    

        #     if 'max_conc' in conc and 'min_conc' in conc:

        #         if conc['max_conc'] == conc['min_conc']:
        #             self.units = conc['max_conc']
        #         else:
        #             self.units = self.units + conc['min_conc'] + '-' + conc['max_conc']
        #     else:
        #         if 'max_conc' in conc:
        #              self.units = conc['max_conc']
        #         if 'min_conc' in conc:
        #              self.units = conc['min_conc']                        
                
        #     self.units = self.units + ' ' + conc['conc_units']  

        
        # if vol:
        #     if not vol['vol_units']:
        #         return 'no Volume units specified for %s' % self['name']
        #     if 'max_vol' not in vol and 'min_vol' not in vol:
        #         return 'enter Volume units for %s' % self['name']

        #     if 'max_vol' in vol and 'min_vol' in vol:

        #         if vol['max_vol'] == vol['min_vol']:
        #             self.units = self.units + ', ' + vol['max_vol']
        #         else:
        #             self.units = self.units + ', ' + vol['min_vol'] + '-' + vol['max_vol']

        #     else:
        #         if 'max_vol' in vol:
        #              self.units = vol['max_vol']
        #         if 'min_vol' in vol:
        #              self.units = vol['min_vol']          
            
        #     self.units = self.units + ' ' + vol['vol_units'] 

        # if mass:
        #     if not mass['mass_units']:
        #         return 'no mass units specified for %s' % self['name']
        #     if 'max_mass' not in mass and 'min_mass' not in mass:
        #         return 'enter mass units for %s' % self['name']

        #     if 'max_mass' in mass and 'min_mass' in mass:

        #         if mass['min_mass'] == mass['max_mass']:
        #             self.units = self.units + ', ' + mass['max_mass']
        #         else:
        #             self.units = self.units + ', ' + mass['min_mass'] + '-' + mass['max_mass']

        #     else:
        #         if 'max_mass' in mass:
        #              self.units = mass['max_mass']
        #         if 'min_mass' in mass:
        #              self.units = mass['min_mass']

        #     self.units = self.units + ' ' + mass['mass_units']

        # if shorthand == True:
        #     self.units = self.units.replace('nanograms','ng') 
        #     self.units = self.units.replace('micrograms','ug')    
        #     self.units = self.units.replace('milligrams','mg')    
        #     self.units = self.units.replace('grams','g')  
        #     self.units = self.units.replace('kilograms','kg') 
        #     self.units = self.units.replace('nanoLiter','ng') 
        #     self.units = self.units.replace('microLiter','ul')    
        #     self.units = self.units.replace('microliter','ul')    
        #     self.units = self.units.replace('milliLiter','ml')    
        #     self.units = self.units.replace('Liters','L')
        #     self.units = self.units.replace('nanoMolar','nM') 
        #     self.units = self.units.replace('microMolar','uM')    
        #     self.units = self.units.replace('milliMolar','mM')    
        #     self.units = self.units.replace('Molar','M')
        #     self.units = self.units.replace('nanomole','nm') 
        #     self.units = self.units.replace('micromole','um')    
        #     self.units = self.units.replace('millimole','mm')    
        #     self.units = self.units.replace('mole','m')
        # return self.units

class Machine(NodeBase):

    def __init__(self, protocol, action=None, data=None, **kwargs):
        self.action = action
        super(Machine, self).__init__(protocol, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        
    def get_absolute_url(self):
        return "#NDF"
        #return reverse("machine_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.action.step.slug, 'action_slug':self.action.slug, 'machine_slug':self.slug  })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.action.step['name'], self.action['name'], self['name'])

    @property
    def parent(self):
        return self.action

    @property
    def label(self):
        return settify(self, shorthand = True)




class Action(NodeBase):

    
    def __init__(self, protocol, step=None, data=None, **kwargs):
        self.step = step
        super(Action, self).__init__(protocol, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.            
    
    def update_data(self, data={}, **kwargs):
        super(Action, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        #print data['name']

        MACHINE_VERBS = ['heat', 'chill', 'centrifuge', 'agitate', 'collect', 'cook', 'cool', 'electrophorese', 'incubate', 'shake', 'vortex']

        if 'component - list' in data:                          # CLEANING UP DATA
            data['components'] = data.pop("component - list")

        if 'components' in data:                                # Convert dictionaries into Component Objects
            self['components'] = [ Component(self.protocol, action=self, data=c) for c in data['components'] ]

        if not self['name']:                # Action default name should be the same as the verb
            self['name'] = self['verb']

        if 'verb' in data and data['verb'] in MACHINE_VERBS:            # MAKE SURE THERE IS SUPPOSED TO BE A MACHINE ATTR

            if not 'machine' in data:
                print "NO SUCH DATA"
                data['machine'] = {}
                MACHINE_ATTRIBUTES = ['min_time', 'max_time', 'time_comment', 'time_units','min_temp', 'max_temp', 'temp_comment', 'temp_units','min_speed', 'max_speed', 'speed_comment', 'speed_units']
                for item in MACHINE_ATTRIBUTES:
                    if item in data:
                        data['machine'][item] = data.pop(item)

            self['machine'] = Machine(self.protocol, action=self, data=data['machine'])

    #def set_name(self):
    #    self['name'] = self['verb']

    def get_absolute_url(self):
        print "ACTION ABSOLUTE URL"
        return reverse("action_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.step.slug, 'action_slug':self.slug })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.step['name'], self['name'])

    @property
    def parent(self):
        return self.step

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


class Step(NodeBase):

    def update_data(self, data={}, **kwargs):
        super(Step, self).update_data(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

        if 'actions' in data:
            self['actions'] = [ Action(self.protocol, step=self, data=a) for a in data['actions'] ]
        else:
            self['actions'] = []

        # UPDATE DURATION AT THE SAME TIME
        duration = 0
        for action in self['actions']:
            if 'duration' in action:
                duration += int(action['duration'])

        self['duration'] = duration

    def get_absolute_url(self):
        #return "serious_URL_STUFF"
        return reverse("step_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self['objectid'] })

    @property
    def title(self):
        return "%s - %s" % (self.protocol.name, self['name'])

    #def get_hash_id(self, size=6, chars=string.ascii_lowercase + string.digits):
    #    '''Always returns a unique ID in the protocol'''
    #    uid_list = []
    #    uid = ''.join(random.choice(chars) for x in range(size))
    #    return uid



class ProtocolIngest(Protocol):
    '''Used for loading protocols from JSON formatted text files.'''

    class Meta:
        db_table = 'protocols_protocol'

    def read_data(self, *args):
        filename = str(args[0])
        self.data = open(filename, 'r').read()
        if self.data:
            return self.data
        else:
            print 'no data loaded'




