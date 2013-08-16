from django.db import models
from django.contrib.auth.models import User
from protocols.models import Protocol, Action, Step
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
import django.utils.simplejson as json
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
#from protocols.utils import MANUAL_VERBS
from core.models import SlugStampMixin

from schedule.models import Calendar
from workflow.models import Workflow


class Experiment(SlugStampMixin, TimeStampedModel):
    '''
    An Experiment is an execution of Workflows
    '''
    user = models.ForeignKey(User)
    # calendar = models.ForeignKey(Calendar)
    workflow = models.ForeignKey(Workflow)    # <- NEEDS TO BE ADDED TO THE MODEL
    name = models.CharField(_("Experiment Name"), max_length=255)
    data = JSONField(blank=True, null=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)

    def save(self,*args,**kwargs):
    	new_slug = self.generate_slug()
    	if self.slug != new_slug:
    		self.slug = new_slug

    	super(Experiment,self).save(*args,**kwargs)	








# Create your models here.

#   Commenting out for now until this is formally ready to be added and all the fields are worked out
#

# class Meta: 
#         proxy = True

#     def __init__(self, *args, **kwargs):
#         super(Experiment, self).__init__(*args, **kwargs)
    
#         self.agraph = pgv.AGraph(ranksep = '0.2')  

#         self.pks = [self.nodes[r].pk for r in self.get_acti



# class Experiment(TimeStampedModel):
#     experimentist = models.ForeignKey(User, blank=True, null=True)
#     workflow = models.ForeignKey(Workflow)
#     owner = models.ForeignKey(Organization)
#     name = models.CharField(_("Name"), max_length=255, unique=True)
#     slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
#     duration = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
#     description = models.TextField(_("Description"), blank=True, null=True)
#     experiment_data = JSONField(blank=True, null=True)


# class Stoichieometry(Protocol, Experiment):
#   number_of_tubes = 




