from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Protocol(TimeStampedModel):

    parent = models.ForeignKey("self", blank=True, null=True)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), blank=True, null=True)
    duration_in_seconds = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
    published = models.BooleanField(_("Published"))
    public = models.BooleanField(_("Public"))
    owner = models.ForeignKey(User)
    company = models.CharField(_("Company"), max_length=100, blank=True, null=True)
    version = models.CharField(_("Version"), max_length=100, blank=True, null=True)
    raw = models.TextField()

    # reference fields
    url = models.URLField(_("URL"), max_length=255, null=True, blank=True)
    PMID = models.CharField(_("PMID"), max_length=255, null=True, blank=True)
    DOI = models.CharField(_("DOI"), max_length=255, null=True, blank=True)
    document_id = models.CharField(_("Document ID"), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Protocol, self).save(*args, **kwargs)
        if not self.slug:
            slug = slugify(self.name)
            pv = self.protocolversion_set.create()
            self.slug = "{0}-v{1}".format(slug, pv.pk)
            self.save()


class ProtocolVersion(TimeStampedModel):

    protocol = models.ForeignKey(Protocol)
    version_id = models.IntegerField(null=True, blank=True)
