from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.db import models
# from django.db.models import ObjectDoesNotExist
# from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from jsonfield import JSONField

# from protocols.models import Protocol
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
    name = models.CharField(_("Name"), max_length=255, unique=True)
    htype = models.CharField(_("History Type"), max_length=10, choices=HISTORY_EVENT_CHOICES, default='EDIT')
    # keyword = models.CharField(_("Keyword"), max_length=10 )
    # description = models.TextField(_("Description"), blank=True, null=True)
    data = JSONField(_("Data"), blank=True)
    protocol = models.ForeignKey('protocols.Protocol')
    org = models.ForeignKey(Organization, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    # slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.name

    def history_add_event(self, node_id, data={}):
        '''
        Data was added to the Item
        '''
        self.data.update({'id':node_id, 'event':"add", "data": data })
        self.name = "add"

    def history_update_event(self, node_id, data={}):
        '''
        Data was updated in the Item
        '''
        self.data.update({'id':node_id, 'event':"update", "data": data })
        self.name = "update"

    def history_delete_event(self, node_id, data={}):
        '''
        Data was deleted from the Item
        '''
        self.data.update({'id':node_id, 'event':"delete", "data": data })
        self.name = "delete"

    def history_clone_event(self, node_id, data={}):
        '''
        Data was cloned from the Item
        '''
        self.data.update({'id':node_id, 'event':"clone", "data": data })
        self.name = "clone"    

    def history_create_event(self, node_id, data={}):
        '''
        Data was created from the Item
        '''
        self.data.update({'id':node_id, 'event':"create", "data": data })
        self.name = "create"        


'''
HISTORY DATA FORMAT

[
    {'id':"XXXXXX", 'event':"add", data: {} },
    {'id':"XXXXXX", 'event':"update", data: {} },
    {'id':"XXXXXX", 'event':"delete" },
]
'''
