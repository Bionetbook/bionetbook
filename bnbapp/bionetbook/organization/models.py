from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from core.models import SlugStampMixin

class Organization(SlugStampMixin, TimeStampedModel):
    name = models.CharField(_("Name"), max_length="60")
    slug = models.SlugField(_("Slug"), max_length="60", null=True, blank=True)
    members = models.ManyToManyField(User, through='Membership')

    def __unicode__(self):
        return self.name

    ##########
    # URLs

    def create_protocol_url(self):
        return reverse("protocol_create", kwargs={'owner_slug':self.slug})

    def organization_protocol_list(self):
        return reverse("organization_main", kwargs={'owner_slug':self.slug})

    def get_absolute_url(self):
        return reverse("organization_main", kwargs={'owner_slug':self.slug})


class Membership(TimeStampedModel):
    user = models.ForeignKey(User)
    org = models.ForeignKey(Organization)
    role = models.CharField(max_length=1, choices=(('r', 'Viewer'),('w', 'Editor'),('a', 'Administrator')))

    def __unicode__(self):
        return self.user.username + " - " + self.org.name

