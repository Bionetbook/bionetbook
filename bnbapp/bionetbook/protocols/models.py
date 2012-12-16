from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import django.utils.simplejson as json
from jsonfield import JSONField

from django_extensions.db.models import TimeStampedModel
import math


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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Protocol, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.
        if not self.slug:
            self.slug = self.generate_slug()
            self.save()

    def generate_slug(self):
        slug = slugify(self.name)
        try:
            Protocol.objects.get(slug=slug)
            return "%s-%d" % (slug, self.pk)
        except ObjectDoesNotExist:
            return slug

    def get_absolute_url(self):
        return reverse("protocol_detail", kwargs={'protocol_slug': self.slug})

    # def get_data(self):
    #     if self.data:
    #         return json.loads(self.data)
    #     return None

    def read_data(self, *args):
        filename = str(args[0])
        self.data = open(filename, 'r').read()
        if self.data:
            return self.data
        else:
            print 'no data loaded'
            

    #@property
    #def actions(self):
    #  self.  fr()om actions.models import Action
    #    return Action.objects.filter(step__protocol=self)

    @property
    def steps(self):
        data = self.data
        if data:
            return data['steps']
        return []

    def get_num_steps(self):
        return len(self.steps)

    def get_num_actions(self):
        return [len(s['actions']) for s in self.steps]

    def get_actions_by_step(self):
        actions_by_step = []
        for stepnum in range(0, self.get_num_steps()):
            tmp = [self.steps[stepnum]['actions'][r]['verb'] for r in range(0, self.get_num_actions[stepnum])]
            actions_by_step.append(tmp)
        return actions_by_step

    def get_action_tree(self):
        action_tree = []
        for stepnum in range(0, self.get_num_steps()): # traversign all steps
            for actionnum in range(0, len(self.steps[stepnum]['actions'])): # traversing all actions per step
                action_tree.append([stepnum, actionnum, self.steps[stepnum]['actions'][actionnum]['verb']])
        
        return action_tree

    def get_schedule_data(self):
        time_atts = ('verb','min_time','max_time','time_units','duration_comment')
        actions_sequence =[]
        # traversing all step and action nodes in the protocol:
        
        for stepnum in range(0, self.get_num_steps()): # traversign all steps
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



class ComponentBase(object):
    """Base class for the protocol components"""

    keylist = ['name','objectid']

    def __init__(self, data=None, **kwargs):
        for item in self.keylist:
            if item in kwargs:
                setattr(self, item, kwargs[item])
            elif item in data:
                setattr(self, item, data[item])
            else:
                setattr(self, item, "")

    def __json(self):
        return self.__dict__


class Verb(ComponentBase):
    pass


class Action(ComponentBase):
    pass


class Step(ComponentBase):
    pass    



