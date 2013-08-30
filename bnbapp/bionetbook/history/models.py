from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.db import models
# from django.db.models import ObjectDoesNotExist
# from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from jsonfield import JSONField

from protocols.models import Protocol
from organization.models import Organization
# Create your models here.

HISTORY_EVENT_CHOICES = (
    ('EDIT', 'Edit Event'),
    ('WORK', 'Workflow Event'),
    ('EXPR', 'Experiment Event'),
)

class History(TimeStampedModel):
    '''
    History log attached to the Project
    '''
    htype = models.CharField(_("History Type"), max_length=10, choices=HISTORY_EVENT_CHOICES, default='EDIT')
    # keyword = models.CharField(_("Keyword"), max_length=10 )
    # description = models.TextField(_("Description"), blank=True, null=True)
    data = JSONField(_("Data"), blank=True, null=True)
    protocol = models.ForeignKey(Protocol)
    org = models.ForeignKey(Organization, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    # slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.name

    def __init__(self, old_state, new_state, htype, *args, **kwargs):
        super(History, self).__init__(*args, **kwargs)
        self.old = old_state
        self.new = new_state
        self.protocol = self.old
        self.org = old_state.owner
        self.user = old_state.author
        self.htype = htype
        self.hdf  = []
        self.diff_protocol_keys()
        self.diff_dict()

    def diff_protocol_keys(self):
        d = DataDiffer(self.old.__dict__, self.new.__dict__)
        cloned = ['name', 'slug', 'pk']
        
        # Naming events:
        if [item for item in cloned if item in d.changed()]:
            self.log_item(objectid = self.old.pk, event = 'cloned', data = self.new.pk)

        if 'user' in d.changed():
            self.log_item(objectid = self.old.pk, event = 'forked', data = self.new.author)
            self.log_item(objectid = self.new.pk, event = 'created', data = self.new.author)

        if "published" in d.changed():
            self.log_item(objectid = self.old.pk, event = 'changed published', data = self.new.published)

        if "public" in d.changed():
            self.log_item(objectid = self.old.pk, event = 'changed public', data = self.new.public)    

        if "description" in d.changed():
            self.log_item(objectid = self.old.pk, event = 'updated', data = self.new.description) 
    
        
    def log_item(self, objectid = None, event = None, data = None):
        self.hdf.append({"objectid": objectid,
                   "event": event,   
                   "data": data  
                   })

    def diff_dict(self, objid= None):
        '''this method takes a dict and finds the differences in it catching the following diffs:
            key-value pairs: 
            triggered by a unicode / int / float / str type. 
            finds the added, removed, changed key value pairs and creates a log for each change
            
            list objects:
            triggered by list type. calls the diff_list method
        '''

        if not objid: # if dict is protocol.data:
            obj_old = self.old.data
            obj_new = self.new.data
            print "diffing data_a and data_b"
        
        else: # all other dicts in protocol.nodes
            obj_old = self.old.nodes[objid]
            obj_new = self.new.nodes[objid] 
            print "diffing %s, %s "% (obj_old['name'], obj_new['name'])

        diff = DataDiffer(obj_old, obj_new) ## diff the step content

        all_keys = set(obj_old.keys()).union(set(obj_new.keys()))

        for key in all_keys:
            if key in diff.changed():
                if isinstance(obj_old[key], list):       
                    self.diff_list(obj_old[key], obj_new[key])

                if isinstance(obj_old[key], (int, float, unicode, str)):
                    self.log_item(objectid = objid, event = "edit", data = {key: obj_new[key]})
                    # print "logged changed %s, %s "% (objid, obj_new[key])
                
            if key in diff.added():
                self.log_item(objectid = objid, event = "add", data = obj_new[key])
                # print "logged add %s, %s "% (objid, obj_new[key])
            
            if key in diff.removed():
                self.log_item(objectid = objid, event = "remove", data = obj_old[key])                
                # print "logged remove%s, %s "% (objid, obj_new[key])

    def diff_list(self, list_a, list_b):         
        ''' this method takes a list of object ids and compares it between the old and the new list. 
            it will catch a few events: 
            1. turns the list of objects into a dict of objectids for ease of compare
            2. finds the added removed or edited objects in each list
            3. for added or removed objects it triggers a log event
            4. for changed objects it recurses to diff_dict'''

        old_list = dict((item['objectid'],item) for item in list_a)
        new_list = dict((item['objectid'],item) for item in list_b)
        
        # find changes between list objects (add, delete update)        
        diff_list_items = DataDiffer(old_list, new_list)
        changed = diff_list_items.changed()
        added = diff_list_items.added()
        removed = diff_list_items.removed()
        
        ### Place Holder for finding chaned Order in list ###

        all_objectids = set(old_list.keys()).union(set(old_list.keys()))
        for objid in all_objectids:
            if objid in added: 
                self.log_item(objectid = objid, event = 'add', data = self.new.nodes[objid])
                # print "logged add%s, %s "% (objid, self.new.nodes[objid])

            if objid in removed:
                self.log_item(objectid = objid, event = 'remove', data = self.old.nodes[objid])
                # print "logged remove%s, %s "% (objid, self.old.nodes[objid])
            
            if objid in changed: 
               self.diff_dict(objid) # recursive call. 
               # print 'recursing dict %s' %objid 

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

'''
HISTORY DATA FORMAT

[
    {'id':"XXXXXX", 'event':"add", data: {} },
    {'id':"XXXXXX", 'event':"update", data: {} },
    {'id':"XXXXXX", 'event':"delete" },
]
'''
