from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from protocol.models import Protocol
# Create your models here.

HISTORY_TYPE_CHOICES = (
    ('EDIT', 'Edit Event Log'),
    ('WORK', 'Workflow Event'),
    ('EXPR', 'Experiment Event'),
)

class History(TimeStampedModel):
    '''
    History log attached to the Project
    '''
    htype = models.CharField(_("Type"), max_length=10, choices=HISTORY_TYPE_CHOICES, default='NOTE')
    # description = models.TextField(_("Description"), blank=True, null=True)
    data = models.TextField(_("Data"), blank=True, null=True)
    protocol = models.ForeignKey(Protocol)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.name
