from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from protocols.models import Protocol


class Step(TimeStampedModel):

    protocol = models.ForeignKey(Protocol)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    raw = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Step, self).save(*args, **kwargs)
        if not self.slug:
            # TODO - make unique within this Protocol
            slug = slugify(self.name)
            try:
                Step.objects.get(slug=slug, protocol=self.protocol)
                count = self.protocol.step_set.filter(slug=slug).count()
                self.slug = "{0}-{1}".format(slug, count)
            except ObjectDoesNotExist:
                self.slug = slug
            self.save()

    def get_absolute_url(self):
        return reverse('step_detail',
            kwargs={'protocol_slug': self.protocol.slug, 'slug': self.slug})
