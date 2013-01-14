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


class Protocol(TimeStampedModel):

    #STATUS_DRAFT = "draft"
    #STATUS_PUBLISHED = "published"
    #STATUS = (
    #    (STATUS_DRAFT, _(STATUS_DRAFT)),
    #    (STATUS_PUBLISHED, _(STATUS_PUBLISHED)),
    #)

    parent = models.ForeignKey("self", blank=True, null=True)
    owner = models.ForeignKey(User)
    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    #organization = models.CharField(_("Orginization"), max_length=100, blank=True, null=True)
    raw = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # protocol_input = models.CharField(_("Input"), max_length=255, unique=True)
    # protocol_output = models.CharField(_("Output"), max_length=255, unique=True)

    #status = models.CharField(_("Status"), max_length=30, blank=True, null=True, default=STATUS_DRAFT, choices=STATUS)
    #version = models.CharField(_("Version"), max_length=100, blank=True, null=True)

    # reference fields
    #url = models.URLField(_("URL"), max_length=255, null=True, blank=True)
    #PMID = models.CharField(_("PMID"), max_length=255, null=True, blank=True)
    #DOI = models.CharField(_("DOI"), max_length=255, null=True, blank=True)
    #document_id = models.CharField(_("Document ID"), max_length=255, null=True, blank=True)


    def __init__(self, *args, **kwargs):
        self.data = {}
        super(Protocol, self).__init__(*args, **kwargs)

        if not self.data:
            self.data={}

        self.steps_data = []


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.set_data_ids()
        self.set_data_slugs()

        if self.data:
            # NEED TO RETURN STEPS TO JSON
            self.data['steps'] = self.steps

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

                if 'component - list' in action.keys():        
                    for reagent in action['component - list']:
                        if 'objectid' in reagent: # hasattr doesn't work here I think because of unicode
                            uid_list.append(reagent['objectid'])          

        if uid not in uid_list:
            return uid

        return self.get_hash_id(size, chars)

    def rebuild_steps(self):
        if self.data and 'steps' in self.data:
            self.steps_data = [ Step(protocol=self, data=s) for s in self.data['steps'] ]

    ###########
    # Validators

    def set_data_ids(self):
        for step in self.steps:
            if not step['objectid']:
                step['objectid'] = self.get_hash_id()

            for action in step['actions']:
                if not action['objectid']:
                    action['objectid'] = self.get_hash_id()
                
                if 'component - list' in action.keys():
                    for reagent in action['component - list']:
                        if 'objectid' not in reagent.keys():
                            reagent['objectid'] = self.get_hash_id()




    def set_data_slugs(self):
        for step in self.steps:
            if not step['slug']:
                step['slug'] = slugify(step['objectid'])

            for action in step['actions']:
                if 'slug' in action and not action['slug']:
                    action['slug'] = slugify(action['objectid'])

    ###########
    # Properties

    @property
    def steps(self):
        if not self.steps_data:
            self.rebuild_steps()
        return self.steps_data


    @property
    def components(self):
        result = {}
        for step in self.steps:
            result[step['objectid']] = step

            for action in step['actions']:
                result[action['objectid']] = action

        return result


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

    # def get_verb_by_tree(self, **kwargs):
        
    #     # test if kwargs pair is in protocol:

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
        self.needed_reagents = []
        
        if self.data['components-location'][0] > 0:  # check if there are components in the protocol:
            for l in self.data['components-location']: # iterate over all step,action locations where there are components
                components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]]['component - list']) 
                for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['reagent_name']
                    objectid = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['objectid']
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
        self.verb_reagents = {}
        for l in self.data['components-location']: # iterate over all step,action locations where there are components 
            components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]]['component - list']) # iterate over reagents
            verb = self.steps[l[1]]['actions'][l[2]]['verb']
            verbid = self.steps[l[1]]['actions'][l[2]]['objectid']
            if out_label == 'literal':
                self.verb_reagents[verbid]=[]
            if out_label == 'objectid':
                self.verb_reagents[verbid]=[]

            for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['reagent_name']
                    if 'total volume' in reagent_name.lower():
                        continue

                    objectid = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['objectid']
                    if out_label == 'literal':
                        self.verb_reagents[verbid].append(reagent_name)
                    if out_label == 'objectid':
                        self.verb_reagents[verbid].append(objectid)
        
        return self.verb_reagents   

    def objectid2name(self, objid, **kwargs):
    
        ''' function takes in a protocol instance (self) and an objid. If the objid is not in the protocol instance, a False is returned. 
        if the objid is in the protocol it returns a list:
        rank = True : step action or reagent
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
        def unify(units_dict, shorthand = True):

            units = ''

            conc = dict((k, v) for k, v in units_dict.iteritems() if 'conc' in k)
            vol = dict((k, v) for k, v in units_dict.iteritems() if 'vol' in k)
            mass = dict((k, v) for k, v in units_dict.iteritems() if 'mass' in k)

            if conc:
                if conc['max_conc'] == conc['min_conc']:
                    units = conc['max_conc']
                else:
                    units = units + conc['min_conc'] + '-' + conc['max_conc']           
                
                units = units + ' ' + conc['conc_units']  

            
            if vol:
                if vol['max_vol'] == vol['min_vol']:
                    units = units + ', ' + vol['max_vol']
                else:
                    units = units + ', ' + vol['min_vol'] + '-' + vol['max_vol']               
                
                units = units + ' ' + vol['vol_units'] 

            if mass:
                if mass['min_mass'] == mass['max_mass']:
                    units = units + ', ' + mass['max_mass']
                else:
                    units = units + ', ' + mass['min_mass'] + '-' + mass['max_mass']

                units = units + ' ' + mass['mass_units']

            if shorthand == True:
                units = units.replace('nanograms','ng') 
                units = units.replace('micrograms','ug')    
                units = units.replace('milligrams','mg')    
                units = units.replace('grams','g')  
                units = units.replace('kilograms','kg') 
                units = units.replace('nanoLiter','ng') 
                units = units.replace('microLiter','ul')    
                units = units.replace('microliter','ul')    
                units = units.replace('milliLiter','ml')    
                units = units.replace('Liters','L')
                units = units.replace('nanoMolar','nM') 
                units = units.replace('microMolar','uM')    
                units = units.replace('milliMolar','mM')    
                units = units.replace('Molar','M')
                units = units.replace('nanomole','nm') 
                units = units.replace('micromole','um')    
                units = units.replace('millimole','mm')    
                units = units.replace('mole','m')
            return units

        default_setting = {}
        default_setting['objectid'] = objid
        default_setting['rank'] =  'None'
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
        steps_by_id = [self.steps[r]['objectid'] for r in range(self.get_num_steps)]
        
        actions_by_id = self.get_action_tree('objectid')
        actions = [actions_by_id[r][2] for r in range(len(actions_by_id))]

        reagent_by_objectid = self.get_reagent_data('objectid')
        reagents_by_id = [reagent_by_objectid[r][0] for r in range(len(reagent_by_objectid))]

        # find what rank of objectid:
        if objid in steps_by_id:
            outDict['rank'] =  'step'
            outDict['name'] = steps_by_id.index(objid) 
            outDict['location'] = [steps_by_id.index(objid)]
            outDict['object_data']  = self.data['steps'][outDict['location'][0]]
            # outDict['slug'] = 
        
        if objid in actions:
            outDict['rank'] = 'action'
            outDict['name'] = self.get_action_tree()[actions.index(objid)][2]
            outDict['location'] = actions_by_id[actions.index(objid)][0:2]
            outDict['object_data'] = self.data['steps'][outDict['location'][0]]['actions'][outDict['location'][1]]


        if objid in reagents_by_id:
            outDict['rank'] = 'reagent'
            outDict['name'] = self.get_reagent_data('name_objectid')[reagents_by_id.index(objid)][0]
            outDict['location'] = self.get_reagent_data('detail')[reagents_by_id.index(objid)][1:3]
            s = self.get_reagents_by_action()
            for k,v in s.items():
                if objid in v:
                    reagent_order = s[k].index(objid)

            outDict['location'].append(reagent_order)
            outDict['object_data'] = self.data['steps'][outDict['location'][0]]['actions'][outDict['location'][1]]['component - list'][outDict['location'][2]]
        

        if kwargs:    
        # Return general requensts:   
            if 'attributes' in kwargs and kwargs['attributes'] == True: 
                outDict['attributes'] = outDict['object_data'].keys()
            
            if 'units' in kwargs and kwargs['units'] == True:
                outDict['units'] = unify(outDict['object_data'])

            if 'parents' in kwargs and kwargs['parents'] == True:
                tmp = self.get_objectid(outDict['location'][0], outDict['location'][1])
                if outDict['rank'] =='step':
                    outDict['parents'] = 'protocol'
                if outDict['rank'] == 'action':
                    outDict['parents'] = tmp[0]
                if outDict['rank'] == 'reagent':
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
           
    def get_schedule_data(self):
        time_atts = ('verb','min_time','max_time','time_units','duration_comment')
        actions_sequence =[]
        # traversing all step and action nodes in the protocol:
        
        for stepnum in range(0, self.get_num_steps): # traversign all steps
            for actionnum in range(0, len(self.steps[stepnum]['actions'])): # traversing all actions per step
                tmp = {}
                # find the time related annotated field that this protcol has
                tagged_fields = [r for r in self.steps[stepnum]['actions'][actionnum].keys() if r in time_atts]
                for l in tagged_fields: # insert the valid tagged_fields into a tmp dict
                    tmp[l] = self.steps[stepnum]['actions'][actionnum][l] 
                actions_sequence.append(tmp)   # append this action dict to the action_sequence list
        return actions_sequence     

    def get_duration_by_line(self):
        # this function can be included in the Quality control after protocol entry.
        # User can enter unspecified times if they can estimate them. 

        schedule_line = []

        for line in self.get_schedule_data():

            out_line = [] 
            out_line.append(line['verb'])
            
            if 'min_time' in line:
                out_line.append(line['min_time'])

            if 'max_time' in line:
                out_line.append(line['max_time'])

            if 'time_units' in line:
                out_line.append(line['time_units'])
                
            if 'duration_comment' in line:
                out_line.append(line['duration_comment'])

            schedule_line.append(out_line) 

        return schedule_line    

    def set_padding(self):

        # self.schedule_padded ='True'
        schedule_padding_list = [['pad', 1, 1, 'minutes', 'Active'] for r in range(0, len(self.get_duration_by_line()))]
        schedule_padded = []
        dur = self.get_duration_by_line()
        # try:
        #     self.schedule_line
        for i in range(0, len(dur)):
            schedule_padded.append(dur[i])
            schedule_padded.append(schedule_padding_list[i])
        # except AttributeError:
        #     print 'get_duration_by_list before adding padding'      

        return schedule_padded   

    def get_duration(self, *args):
        
        if 'padding' in args:
            schedule = self.set_padding()
        else:
            schedule = self.get_duration_by_line()
        active_list = []
        passive_list = []
        total_list= []
        for line in schedule:
            if type(line[1]) == int or line[1][0].isdigit():
                if line[3]=='minutes':
                    total_list.append(float(line[1]))
                if line [3]=='hours':
                    total_list.append(float(line[1])*60)
                if line [3]=='days':
                    total_list.append(float(line[1])*60*24)
                if 'Active'.lower() in line[4].lower():
                    active_list.append(total_list[-1])
                if 'Passive'.lower() in line[4].lower():
                    passive_list.append(total_list[-1])     
            else:
                continue

        total_time = math.ceil(sum(total_list))
        d = divmod(math.ceil(total_time),60)
        pprint_total_time = '{0} hours and {1} minutes'.format(d[0], d[1])
        total_active_time = sum(active_list)            
        total_passive_time = sum(passive_list)  
        if 'literal' in args:
            return pprint_total_time
        else:
            return total_time*60      



class ComponentBase(dict):
    """Base class for the protocol components"""

    keylist = ['name','objectid']

    # ADD _meta CLASS TO USE SOME EXTRA DB-LIKE FUNCTIONALITY

    class Meta:
        def __init__(self, component):
            self.component = component

        def get_all_field_names(self):
            result = self.component.keys()
            result.sort()
            return result

    def __init__(self, protocol, data={}, **kwargs):
        super(ComponentBase, self).__init__(**kwargs)

        self.protocol = protocol

        self['objectid'] = None #self.get_hash_id()
        self['slug'] = None

        self._meta = ComponentBase.Meta(self)

        for item in self.keylist:       # REQUIRED ATTRIBUTES
            self[item] = None

        self.update_data(data)

        if not 'name' in self or not self['name']:
            self.set_name()

    @property
    def slug(self):
        if not self['slug']:
            self['slug'] = slugify(self['objectid'])
        return self['slug']

    def set_name(self):
        self['name'] = self['slug']

    def update_data(self, data={}, **kwargs):
        for key in data:
            self[key] = data[key]

        #for item in kwargs:             # OVERRIDE DATA WITH ANY PARTICULAR KWARGS PASSED
        #    self[item] = kwargs[item]

    def __unicode__(self):
        return self['slug']

    @property
    def title(self):
        return self.protocol.name


class Componenet(ComponentBase):
    pass


class Action(ComponentBase):

    def __init__(self, protocol, step=None, data=None, **kwargs):
        self.step = step
        super(Action, self).__init__(protocol, data=data, **kwargs) # Method may need to be changed to handle giving it a new name.

    def set_name(self):
        self['name'] = self['verb']

    def get_absolute_url(self):
        return reverse("action_detail", kwargs={'protocol_slug': self.step.protocol.slug, 'step_slug':self.step.slug, 'action_slug':self.slug })

    @property
    def title(self):
        return "%s - %s - %s" % (self.protocol.name, self.step['name'], self['name'])


class Step(ComponentBase):

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
        return reverse("step_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self['slug'] })

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
