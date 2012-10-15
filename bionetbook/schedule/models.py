from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
from django.db import models
#from django.db.models import ObjectDoesNotExist
#from django.template.defaultfilters import slugify
#from django.utils.translation import ugettext_lazy as _
from actions.models import Action

from django_extensions.db.models import TimeStampedModel


class Schedule(TimeStampedModel):
    owner = models.ForeignKey(User)
    start = models.TimeField()
    name = models.CharField(_("Name"), max_length=255)


class Event(TimeStampedModel):
    child = models.ForeignKey("self", blank=True, null=True, unique=True)
    schedule = models.ForeignKey(Schedule)
    action = models.ForeignKey(Action)
    summary = models.CharField(_("Summary"), max_length=255)
    description = models.TextField(blank=True, null=True)
    start = models.TimeField()
    end = models.TimeField()
    uid = models.CharField(max_length=255)

