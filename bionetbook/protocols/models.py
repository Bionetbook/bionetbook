from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Protocol(TimeStampedModel):

    parent = models.ForeignKey("self", blank=True, null=True, unique=True)
    name = models.CharField(_("Name"), max_length=255, unique=True)
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
            try:
                Protocol.objects.get(slug=slug)
                self.slug = "{0}-v{1}".format(slug, self.pk)                
            except ObjectDoesNotExist:
                self.slug = slug
            self.save()
            
    def get_absolute_url(self):
        return reverse("protocol_detail", kwargs={'slug': self.slug})