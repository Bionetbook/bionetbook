from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel, AutoSlugField


class Protocol(TimeStampedModel):

    name = models.CharField(_("Name"), max_length=255)
    slug = AutoSlugField(_("Slug"), populate_from="name")
    duration_in_seconds = models.IntegerField(_("Duration in seconds"))
    published = models.BooleanField(_("Published"))
    public = models.BooleanField(_("Public"))
    version = models.CharField(_("Version"), max_length=100)
    owner = models.ForeignKey(User)
    company = models.CharField(_("Company"), max_length=100, blank=True, null=True)
    raw = models.TextField()

    # reference fields
    url = models.URLField(_("Name"), max_length=255, null=True, blank=True)
    PMID = models.CharField(_("PMID"), max_length=255, null=True, blank=True)
    DOI = models.CharField(_("Name"), max_length=255, null=True, blank=True)
    document_id = models.CharField(_("Name"), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name
