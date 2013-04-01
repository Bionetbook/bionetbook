from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class Workflow(TimeStampedModel):
    '''Collection of Protocols for working doing an experiment with'''
    name = models.CharField(_("Name"), max_length=255, unique=True)
    author = models.ForeignKey(User, blank=True, null=True)
    owner = models.ForeignKey(Organization)
    protocols = models.ManyToManyField(Protocol, through='WorkflowProtocol')
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    note = models.TextField(_("Notes"), blank=True, null=True)


class WorkflowProtocol(TimeStampedModel):
    '''Connection model between Protocols and Workflows'''
    protocol = models.ForeignKey(Protocol)
    workflow = models.ForeignKey(Workflow)
    order = models.IntegerField(_("Order or Protocols"), blank=True, null=True)

    def __unicode__(self):
        return self.protocol.name + " - " + self.workflow.name
