from django.db import models
from django.db.models import ObjectDoesNotExist
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from protocols.models import Protocol
from organization.models import Organization
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

    def save(self, *args, **kwargs):
        super(Workflow, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.
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

    def __unicode__(self):
        return self.name

    ##########
    # URLs

    def get_absolute_url(self):
        return reverse("workflow_detail", kwargs={'owner_slug':self.owner.slug, 'workflow_slug': self.slug})

    def get_update_url(self):
        return reverse("workflow_update", kwargs={'owner_slug':self.owner.slug, 'workflow_slug': self.slug})

    def get_delete_url(self):
        return reverse("workflow_delete", kwargs={'owner_slug':self.owner.slug, 'workflow_slug': self.slug})


    ##########
    # Properties

    @property
    def protocol_count(self):
        return 3                # THIS IS TEMP FOR CODING


class WorkflowProtocol(TimeStampedModel):
    '''Connection model between Protocols and Workflows'''
    protocol = models.ForeignKey(Protocol)
    workflow = models.ForeignKey(Workflow)
    order = models.IntegerField(_("Order or Protocols"), default=0)

    def __unicode__(self):
        return self.workflow.name + " - " + self.protocol.name
