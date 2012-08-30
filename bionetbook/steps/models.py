
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, AutoSlugField

from protocols.models import Protocol


class Step(TimeStampedModel):

    protocol = models.ForeignKey(Protocol)
    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(_("Slug"), populate_from="name")
    duration = models.TODO
    raw = models.TextField()

    def __unicode__(self):
        return self.name
