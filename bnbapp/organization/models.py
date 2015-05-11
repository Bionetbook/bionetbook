from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(_("Name"), max_length="60")
    slug = models.SlugField(_("Slug"), max_length="60", null=True, blank=True)
    members = models.ManyToManyField(User, through='Membership')

    def __unicode__(self):
        return self.name

    #def get_absolute_url(self):
    #    return reverse("organization_detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.generate_slug()
            self.save()

    ##########
    # Generators

    def generate_slug(self):
        slug = slugify(self.name)
        try:
            Organization.objects.get(slug=slug)
            return "%s-%d" % (slug, self.pk)
        except ObjectDoesNotExist:
            return slug

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

