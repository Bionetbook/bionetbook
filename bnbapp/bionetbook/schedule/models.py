from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from protocols.models import Protocol, Step, Action

from django_extensions.db.models import TimeStampedModel


class ProtocolSchedule(TimeStampedModel):

    # class Meta: 
    #     proxy = True

    def __init__(self, *args, **kwargs):
        super(ProtocolSchedule, self).__init__(*args, **kwargs)
        owner = models.ForeignKey(User)
        uid = models.SlugField(_("UID"), blank=True, null=True, max_length=255)

        start = models.DateTimeField()
        name = models.CharField(_("Name"), max_length=255)
        permitted_protocols = models.ForeignKey(Protocol)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)
        if not self.uid:
            uid = slugify("bnb-%d" % self.id)
            try:
                Schedule.objects.get(uid=uid)
                self.uid = "{0}-{1}".format(uid, self.pk)
            except ObjectDoesNotExist:
                self.uid = uid
            self.save()

    #def get_absolute_url(self):
    #    return reverse("schedule_detail", kwargs={'schedule_uid': self.uid})


class Event(TimeStampedModel):
    child = models.ForeignKey("self", blank=True, null=True, unique=True)
    schedule = models.ForeignKey(ProtocolSchedule)
    # action = models.ForeignKey(Action, blank=True, null=True)
    name = models.CharField(_("Summary"), max_length=255)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    uid = models.SlugField(_("UID"), blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if not self.uid:
            uid = slugify("%s-%s" % (self.schedule.uid, self.id))
            try:
                Event.objects.get(uid=uid)
                self.uid = "{0}-{1}".format(uid, self.pk)
            except ObjectDoesNotExist:
                self.uid = uid
            self.save()

    #def get_absolute_url(self):
    #    return reverse("event_detail", kwargs={'event_uid': self.uid})

