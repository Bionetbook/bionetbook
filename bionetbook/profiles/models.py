from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):

    user = models.OneToOneField(User)
    mobile = models.CharField(_("Mobile"), max_length="15", null=True, blank=True)
    address_1 = models.CharField(_("Address 1"), max_length=100, null=True, blank=True)
    address_2 = models.CharField(_("Address 2"), max_length=100, null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    state = USStateField(_("State"), null=True, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=10, null=True, blank=True)

    def __unicode__(self):
        user = self.user
        return "{0} {1}".format(user.first_name, user.last_name)

    def get_absolute_url(self):

        return reverse("profile_detail", kwargs={"pk": self.pk})
