import string
import random
import math

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
        super(Protocol, self).__init__(*args, **kwargs)
        self.steps_data = []


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.set_data_ids()
        self.set_data_slugs()

        # NEED TO RETURN STEPS TO JSON
        self.data['steps'] = self.steps

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





    # @property
    # def components(self):
    #     result = {}
    #     for step in self.steps:
    #         result[step['objectid']] = step

    #         for action in step.actions:
    #             result[action['objectid']] = action

    #     return result


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

    def get_reagents_by_action(self, display='objectid'):
        self.verb_reagents = {}
        for l in self.data['components-location']: # iterate over all step,action locations where there are components 
            components_per_cur_list = len(self.steps[l[1]]['actions'][l[2]]['component - list']) # iterate over reagents
            verb = self.steps[l[1]]['actions'][l[2]]['verb']
            verbid = self.steps[l[1]]['actions'][l[2]]['objectid']
            # if display == 'literal':
            #     self.verb_reagents[verb]=[]
            if display == 'objectid':
                self.verb_reagents[verbid]=[]

            for r in range(0,components_per_cur_list):
                    reagent_name = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['reagent_name']
                    objectid = self.steps[l[1]]['actions'][l[2]]['component - list'][r]['objectid']
                    # if display == 'literal':
                    #     self.verb_reagents[verb].append(reagent_name)
                    if display == 'objectid':
                        self.verb_reagents[verbid].append(objectid)
        
        return self.verb_reagents   

    def objectid2name(self, objid, **kwargs):
    
        ''' function takes in a protocol instance (self) and an objid. If the objid is not in the protocol instance, a False is returned. 
        if the objid is in the protocol it returns a list:
        rank: step action or reagent
        name: returns the name of the object.
        location: returns a (step, action) location. If step, it returns a single int.''' 
        
        # make lists of all objectid's:
        steps_by_id = [self.steps[r]['objectid'] for r in range(self.get_num_steps)]
        
        actions_by_id = self.get_action_tree('objectid')
        actions = [actions_by_id[r][2] for r in range(len(actions_by_id))]

        reagent_by_objectid = self.get_reagent_data('objectid')
        reagents_by_id = [reagent_by_objectid[r][0] for r in range(len(reagent_by_objectid))]

        # find what rank of objectid:
        if objid in steps_by_id:
            rank =  'step'
            name = steps_by_id.index(objid) 
            location = steps_by_id.index(objid) 
            return [rank, name, location]
        
        if objid in actions:
            rank = 'action'
            name = self.get_action_tree()[actions.index(objid)][2]
            location = actions_by_id[actions.index(objid)][0:2]
            return [rank, name, location]
        
        if objid in reagents_by_id:
            rank = 'reagent'
            name = self.get_reagent_data('name_objectid')[reagents_by_id.index(objid)][0]
            location = self.get_reagent_data('detail')[reagents_by_id.index(objid)][1:3]
            return [rank, name, location]
        
        else:
            return False   
           
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

    def __init__(self, data=None, **kwargs):
        super(ComponentBase, self).__init__(**kwargs)

        for item in self.keylist:
            self[item] = None

        for item in data:
            self[item] = data[item]

        for item in kwargs:
            self[item] = kwargs[item]

    def __unicode__(self):
        return self['slug']


class Verb(ComponentBase):
    pass


class Action(ComponentBase):

    def __init__(self, step, data=None, **kwargs):
        self.step = step
        self.objectid = None
        super(Action, self).__init__(data=data, **kwargs) # Method may need to be changed to handle giving it a new name.
        self.slug = self.objectid

    def get_absolute_url(self):
        return reverse("action_detail", kwargs={'protocol_slug': self.step.protocol.slug, 'step_slug':self.step.slug, 'action_slug':self.slug })

    #@property
    #def dump(self):
    #    result = {}
    #    for k,v in self.__dict__.items():
    #        if k not in ['protocol','step']:
    #            result[k] = v
    #    return result


class Step(ComponentBase):

    #actions = []
    #objectid = None

    def __init__(self, protocol, data=None):
        self.protocol = protocol
        self['objectid'] = None #self.get_hash_id()
        self['slug'] = None
        self['actions'] = []

        if data:
            if 'slug' in data:
                self['slug'] = data['slug']

            self['actions'] = [ Action(step=self, data=a) for a in data['actions'] ]

            if 'objectid' in data:
                self['objectid'] = data['objectid']


    def get_hash_id(self, size=6, chars=string.ascii_lowercase + string.digits):
        '''Always returns a unique ID in the protocol'''
        uid_list = []
        uid = ''.join(random.choice(chars) for x in range(size))
        return uid


    def get_absolute_url(self):
        return reverse("step_detail", kwargs={'protocol_slug': self.protocol.slug, 'step_slug':self.slug })

    #@property
    #def __repr__(self):
    #    result = {}
    #    for k,v in self.__dict__.items():
    #        if k not in ['protocol','actions']:
    #            result[k] = v
    #    return result

    #def __repr__(self):
    #    return json.dumps(self.__dict__)


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
