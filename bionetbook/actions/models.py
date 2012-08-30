from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, AutoSlugField

from steps.models import Step


class Action(TimeStampedModel):

    step = models.ForeignKey(Step)
    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(_("Slug"), populate_from="name")
    duration_in_seconds = models.IntegerField(_("Duration in seconds"))
    raw = models.TextField()
    # attributes = TODO

    def __unicode__(self):
        return self.name


