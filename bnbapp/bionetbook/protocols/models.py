from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

import django.utils.simplejson as json

from django_extensions.db.models import TimeStampedModel


class Protocol(TimeStampedModel):

    #STATUS_DRAFT = "draft"
    #STATUS_PUBLISHED = "published"
    #STATUS = (
    #    (STATUS_DRAFT, _(STATUS_DRAFT)),
    #    (STATUS_PUBLISHED, _(STATUS_PUBLISHED)),
    #)

    parent = models.ForeignKey("self", blank=True, null=True)
    owner = models.ForeignKey(User)
    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    #organization = models.CharField(_("Orginization"), max_length=100, blank=True, null=True)
    raw = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    #status = models.CharField(_("Status"), max_length=30, blank=True, null=True, default=STATUS_DRAFT, choices=STATUS)
    #version = models.CharField(_("Version"), max_length=100, blank=True, null=True)

    # reference fields
    #url = models.URLField(_("URL"), max_length=255, null=True, blank=True)
    #PMID = models.CharField(_("PMID"), max_length=255, null=True, blank=True)
    #DOI = models.CharField(_("DOI"), max_length=255, null=True, blank=True)
    #document_id = models.CharField(_("Document ID"), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Protocol, self).save(*args, **kwargs)
        if not self.slug:
            slug = slugify(self.name)
            try:
                Protocol.objects.get(slug=slug)
                self.slug = "%s-%d" % (slug, self.pk)
            except ObjectDoesNotExist:
                self.slug = slug
            self.save()

    def get_absolute_url(self):
        return reverse("protocol_detail", kwargs={'protocol_slug': self.slug})


    def get_data(self):
        if self.data:
            return json.loads(self.data)
        return None

    #@property
    #def actions(self):
    #    from actions.models import Action
    #    return Action.objects.filter(step__protocol=self)

    @property
    def steps(self):
        data = self.get_data()
        if data:
            return data['steps']
        return []



#class Step(object):
#    pass
