from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from jsonfield import JSONField

from protocols.models import Protocol
from steps.models import Step
from verbs.utils import VERB_CHOICES


class Action(TimeStampedModel):

    VERB_CHOICES = VERB_CHOICES

    step = models.ForeignKey(Step)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    verb = models.CharField(max_length=50, choices=VERB_CHOICES)
    verb_attributes = JSONField(blank=True, null=True)
    raw = models.TextField(blank=True, null=True)

    @property
    def protocol(self):
        return Protocol.objects.get(step__action=self)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Action, self).save(*args, **kwargs)
        if not self.slug:
            # TODO - make unique within this Step
            slug = slugify(self.name)
            try:
                Action.objects.get(slug=slug)
                self.slug = "{0}-{1}".format(slug, self.pk)
            except ObjectDoesNotExist:
                self.slug = slug
            self.save()

    def get_absolute_url(self):
        return reverse('action_detail',
            kwargs=dict(protocol_slug=self.protocol.slug, step_slug=self.step.slug, slug=self.slug))
