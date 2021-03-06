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

from protocols.models import Protocol, Step, Action
from workflow.models import Workflow
from experiment.models import Experiment
from django.utils.datastructures import SortedDict

import collections


#from experiment.models import Experiment


class Calendar(TimeStampedModel):
    
    '''
    An Schedule is derived from an Experiment

    data: { 'meta': { 1: "sample description",
                      2: "sample"
                      experiments: [1 ,2, 3]
                    },
            'events': [ {   'id':"bnb-o1-e1-p1-AXBAGS-FFGGAX":,
                            'start':1376957033,
                            'duration':300,
                            'title':"First Action",
                            'protocol':'dna-jalkf',
                            'experiment':'experiment 1',
                            'notes':"",
                            'verb':"mix"
                            'active':"active"
                        },
                        {   'id': "bnb-o1-e1-p1-AXBAGS-GBRISH",
                            'start':1376957033,
                            'duration':500,
                            'title':"First Action",
                            'protocol':'dna-jalkf',
                            'experiment':'experiment 1',
                            'notes':"",
                            'verb':"mix"
                        },
                        {   'id': "bnb-o1-e2-p1-AXBAGS-GBRISH",
                            'start':1376957033,
                            'duration':500,
                            'title':"First Action",
                            'protocol':'dna-jalkf',
                            'experiment':'experiment 1',
                            'notes':"",
                            'verb':"mix"
                        },
                      ]
             }
    '''

    user = models.ForeignKey(User)
    name = models.CharField(_("Calendar Name"), max_length=255)
    data = JSONField(blank=True, null=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        # self.data = {}
        if not self.data:
            # self.data['steps'] = []
            self.full_clean()
            self.data = self.setupCalendar()

        super(Calendar,self).save(*args,**kwargs)

        new_slug = self.generate_slug()

        if not new_slug == self.slug: # Triggered when its a clone method
            self.slug = new_slug
            super(Calendar, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.

    def __unicode__(self):
        return self.name
    
    def events(self):
        return self.data['events']

    def get_absolute_url(self):
        return reverse("single_calendar", kwargs={'pk':self.pk})

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

    def generate_slug(self):
        slug = slugify(self.name)
        if self.pk:
            return "%d-%s" % (self.pk, slug)
        else:
            return slug

    def setupCalendar(self):
        ret = {'meta':{'experiments':[]},'events':[]}
        # userExperimentList = self.user.experiment_set.all()
        # for e in userExperimentList:                    # loop through each experiment for user
        #     protocolList = [Protocol.objects.get(pk=p) for p in e.workflow.data['protocols']]
        #     for p in protocolList:      # loop through each experiments protocols
        #         #stepActionList = zip(p.get_steps(), p.get_actions(), p.get_action_verbs(), p.get_action_durations(), p.get_action_names())
        #         actionList = []
        #         for step in p.data['steps']:
        #             for action in step['actions']:
        #                 #print p.slug + " " + action['objectid']
        #                 if action['physical_commitment']:
        #                     if action['physical_commitment']=="Active" or action['physical_commitment']=="Setup":
        #                         flag = "true"
        #                     else:
        #                         flag = "false"
        #                 else:
        #                     flag = "false"
        #                 actionList.append((step['objectid'],action['objectid'],action['verb'],action['duration'],action['name'],flag))

        #         for element in actionList:
        #             eventObject = {}
        #             eventObject['id'] = 'bnb-o%d-e%d-p%d-%s-%s' % (e.owner.pk,e.pk,p.pk, element[0], element[1])
        #             eventObject['start'] = '0'
        #             if "-" in element[3]:
        #                 eventObject['duration'] = element[3].split('-')[1]
        #             else:
        #                 eventObject['duration'] = element[3]
        #             eventObject['verb'] = element[2]
        #             eventObject['title'] = element[4]
        #             eventObject['protocol'] = p.title
        #             eventObject['experiment'] = e.name
        #             eventObject['notes'] = ""
        #             eventObject['active'] = element[5]
        #             ret['events'].append(eventObject)
        #         if p.pk not in ret['meta']:
        #             ret['meta'][p.pk] = p.description
        return ret

    def addExperiment(self, newExperiment):
        if newExperiment.pk not in self.data['meta']['experiments']:
            events = self.data['events']             
            protocolList = [Protocol.objects.get(pk=p) for p in newExperiment.workflow.data['protocols']]
            for p in protocolList:      # loop through each experiments protocols
                actionList = []
                for step in p.data['steps']:
                    for action in step['actions']:
                        if action['physical_commitment']:
                            if action['physical_commitment']=="Active" or action['physical_commitment']=="Setup":
                                flag = "true"
                            else:
                                flag = "false"
                        else:
                            flag = "false"    
                        actionList.append((step['objectid'],action['objectid'],action['verb'],action['duration'],action['name'],flag))

                for element in actionList:
                    eventObject = {}
                    eventObject['id'] = 'bnb-o%d-e%d-p%d-%s-%s' % (newExperiment.owner.pk, newExperiment.pk,p.pk, element[0], element[1])
                    eventObject['start'] = '0'
                    if "-" in element[3]:
                        eventObject['duration'] = element[3].split('-')[1]
                    else:
                        eventObject['duration'] = element[3]
                    eventObject['verb'] = element[2]
                    eventObject['title'] = element[4]
                    eventObject['protocol'] = p.title
                    eventObject['experiment'] = newExperiment.name
                    eventObject['notes'] = ""
                    eventObject['active'] = element[5]
                    events.append(eventObject)
                if p.pk not in self.data['meta']:
                    self.data['meta'][p.pk] = p.description
            self.data['events'] = events
            self.data['meta']['experiments'].append(newExperiment.pk)
            self.save()   

    def updateCalendar(self, updatedExperiment, workflowUpdated, nameUpdated):
        if workflowUpdated:
            events = self.data['events']
            events = [e for e in events if int(e['id'].split('-')[2][1])!=updatedExperiment.pk]
            print events
            self.data['events'] = events
            self.data['meta']['experiments'].remove(updatedExperiment.pk)
            self.addExperiment(updatedExperiment)
        else:
            if nameUpdated:
                events = self.data['events']
                for e in events:
                    #print int(e['id'].split('-')[2][1])
                    if int(e['id'].split('-')[2][1])==updatedExperiment.pk:
                        e['experiment'] = updatedExperiment.name
                self.save()



    # def expToCalendar(self):  # defaulted to take only 1 experiment
    #     scheduledExperiment = Experiment.objects.get(pk=1)
    #     experimentWorkflow = scheduledExperiment.workflow
    #     protocolList = [Protocol.objects.filter(pk=p).get() for p in experimentWorkflow.data['protocols']]
    #     ret = SortedDict()
    #     for protocol in protocolList:
    #         stepI = 0
    #         stepList = []
    #         for stepI, step in enumerate(protocol.steps): # list of steps 
    #             action = step['actions'][0] # action as a dict
    #             s = SortedDict([('eventId',protocol.pk),('instanceId',0),('verb',action['verb']),('active','true'),
    #                 ('length',5),('container','false'),('stepNumber',stepI+1),('notes',step['technique_comment']),('actionID',action['objectid'])])
    #             stepList.append(s)
    #         ret[protocol.slug] = SortedDict([('container','true'),('title',protocol.title),('protocolID',protocol.pk),('length',protocol.duration),('description',protocol.description),('events',stepList)])
    #     return ret

    # def listExperiments(self):
    #     return [ x['name'] for x in self.data['experiments'] ]




    # def returnCalendar(self):
    #     result = {}

    #     for item in self.data['experiments']:
    #         result[item['name']] = item['schedule']

    #     return result






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

