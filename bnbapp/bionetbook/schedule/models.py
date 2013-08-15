# import math
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
# from protocols.models import Protocol, Step, Action
from django_extensions.db.models import TimeStampedModel
from jsonfield import JSONField

from protocols.models import Protocol
from workflow.models import Workflow
from django.utils.datastructures import SortedDict

import collections


#from experiment.models import Experiment


class Calendar(TimeStampedModel):
    '''
    An Schedule is derived from an Experiment
    '''
    user = models.ForeignKey(User)
    name = models.CharField(_("Calendar Name"), max_length=255)
    data = JSONField(blank=True, null=True)

    def save(self,*args,**kwargs):
        # self.data = {}
        if not self.data:
            self.data['steps'] = []
        super(Calendar,self).save(*args,**kwargs)


    # def dataToCalendar(self):
    #     ret = {}    # return dict
    #     stepsList = []
    #     index = 0
    #     for index, step in enumerate(protocol.data['steps']):       # step is dict
    #         # index +=1
    #         verb = step['actions'][0]['verb']
    #         s = SortedDict([('eventId',Protocol.slug),('instanceId',0),('verb',verb),
    #                 ('active','true'),('length',Protocol.duration),
    #                 ('container','false'),('stepNumber',index),('notes',step['technique_comment'])])
    #         st = "step%s" % index
    #         stepsList.append({st:s})
    #     ret[Protocol.slug] = SortedDict([('container','true'),('title',Protocol.title),('length',Protocol.duration),('description',Protocol.description),('steps',stepsList)])
    #     print ret

    def expToCalendar(self):  # defaulted to take only 1 experiment
        usrExpLst = self.user.experiment_set.all()[0]
        expData = usrExpLst.data
        wrkflw = Workflow.objects.filter(pk=expData['workflow']['pk']).get() 
        protocolList = [Protocol.objects.filter(pk=p).get() for p in wrkflw.data['protocols']]
        ret = SortedDict()
        for protocol in protocolList:
            stepI = 0
            stepList = []
            for stepI, step in enumerate(protocol.data['steps']): # list of steps 
                action = step['actions'][0] # action as a dict
                s = SortedDict([('eventId',protocol.pk),('instanceId',0),('verb',action['verb']),('active','true'),
                    ('length',5),('container','false'),('stepNumber',stepI+1),('notes',step['technique_comment']),('actionID',action['objectid'])])
                stepList.append(s)
            ret[protocol.slug] = SortedDict([('container','true'),('title',protocol.title),('protocolID',protocol.pk),('length',protocol.duration),('description',protocol.description),('events',stepList)])
        return ret
        









# class Schedule(TimeStampedModel):
#     owner = models.ForeignKey(User)
#     protocol = models.ForeignKey(Protocol)
#     start = models.DateTimeField()
#     name = models.CharField(_("Name"), max_length=255)
#     uid = models.SlugField(_("UID"), blank=True, null=True, max_length=255)

#     def __unicode__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         super(Schedule, self).save(*args, **kwargs)
#         if not self.uid:
#             uid = slugify("bnb-%d" % self.id)
#             try:
#                 Schedule.objects.get(uid=uid)
#                 self.uid = "{0}-{1}".format(uid, self.pk)
#             except ObjectDoesNotExist:
#                 self.uid = uid
#             self.save()

#     #def get_absolute_url(self):
#     #    return reverse("schedule_detail", kwargs={'schedule_uid': self.uid})

#     def get_schedule_data(self):
#         time_atts = ('verb','min_time','max_time','time_units','duration_comment')
#         actions_sequence =[]
#         # traversing all step and action nodes in the protocol:
        
#         for stepnum in range(0, self.get_num_steps): # traversign all steps
#             for actionnum in range(0, len(self.steps[stepnum]['actions'])): # traversing all actions per step
#                 tmp = {}
#                 # find the time related annotated field that this protcol has
#                 tagged_fields = [r for r in self.steps[stepnum]['actions'][actionnum].keys() if r in time_atts]
#                 for l in tagged_fields: # insert the valid tagged_fields into a tmp dict
#                     tmp[l] = self.steps[stepnum]['actions'][actionnum][l] 
#                 actions_sequence.append(tmp)   # append this action dict to the action_sequence list
#         return actions_sequence     

#     def get_duration_by_line(self):
#         # this function can be included in the Quality control after protocol entry.
#         # User can enter unspecified times if they can estimate them. 

#         schedule_line = []

#         for line in self.get_schedule_data():

#             out_line = [] 
#             out_line.append(line['verb'])
            
#             if 'min_time' in line:
#                 out_line.append(line['min_time'])

#             if 'max_time' in line:
#                 out_line.append(line['max_time'])

#             if 'time_units' in line:
#                 out_line.append(line['time_units'])
                
#             if 'duration_comment' in line:
#                 out_line.append(line['duration_comment'])

#             schedule_line.append(out_line) 

#         return schedule_line    

#     def set_padding(self):

#         # self.schedule_padded ='True'
#         schedule_padding_list = [['pad', 1, 1, 'minutes', 'Active'] for r in range(0, len(self.get_duration_by_line()))]
#         schedule_padded = []
#         dur = self.get_duration_by_line()
#         # try:
#         #     self.schedule_line
#         for i in range(0, len(dur)):
#             schedule_padded.append(dur[i])
#             schedule_padded.append(schedule_padding_list[i])
#         # except AttributeError:
#         #     print 'get_duration_by_list before adding padding'      

#         return schedule_padded   

#     def get_duration(self, *args):
        
#         if 'padding' in args:
#             schedule = self.set_padding()
#         else:
#             schedule = self.get_duration_by_line()
#         active_list = []
#         passive_list = []
#         total_list= []
#         for line in schedule:
#             if type(line[1]) == int or line[1][0].isdigit():
#                 if line[3]=='minutes':
#                     total_list.append(float(line[1]))
#                 if line [3]=='hours':
#                     total_list.append(float(line[1])*60)
#                 if line [3]=='days':
#                     total_list.append(float(line[1])*60*24)
#                 if 'Active'.lower() in line[4].lower():
#                     active_list.append(total_list[-1])
#                 if 'Passive'.lower() in line[4].lower():
#                     passive_list.append(total_list[-1])     
#             else:
#                 continue

#         total_time = math.ceil(sum(total_list))
#         d = divmod(math.ceil(total_time),60)
#         pprint_total_time = '{0} hours and {1} minutes'.format(d[0], d[1])
#         total_active_time = sum(active_list)            
#         total_passive_time = sum(passive_list)  
#         if 'literal' in args:
#             return pprint_total_time
#         else:
#             return total_time*60      



# class Event(TimeStampedModel):
#     child = models.ForeignKey("self", blank=True, null=True, unique=True)
#     # schedule = models.ForeignKey(ProtocolSchedule)
#     # action = models.ForeignKey(Action, blank=True, null=True)
#     name = models.CharField(_("Summary"), max_length=255)
#     description = models.TextField(blank=True, null=True)
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     uid = models.SlugField(_("UID"), blank=True, null=True, max_length=255)

#     def __unicode__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         super(Event, self).save(*args, **kwargs)
#         if not self.uid:
#             uid = slugify("%s-%s" % (self.schedule.uid, self.id))
#             try:
#                 Event.objects.get(uid=uid)
#                 self.uid = "{0}-{1}".format(uid, self.pk)
#             except ObjectDoesNotExist:
#                 self.uid = uid
#             self.save()

#     #def get_absolute_url(self):
#     #    return reverse("event_detail", kwargs={'event_uid': self.uid})

