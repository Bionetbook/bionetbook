from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from protocols.models import Protocol


class Profile(TimeStampedModel):

    user = models.OneToOneField(User)
    first_name = models.CharField(_("First Name"), max_length="30", null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length="30", null=True, blank=True)
    mobile = models.CharField(_("Mobile"), max_length="15", null=True, blank=True)
    address_1 = models.CharField(_("Address 1"), max_length=100, null=True, blank=True)
    address_2 = models.CharField(_("Address 2"), max_length=100, null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    state = USStateField(_("State"), null=True, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=10, null=True, blank=True)
    #orgs = models.CharField( max_length=100, null=True, blank=True)
    #protocols = models.ManyToManyField(Protocol, through='Organization')

    def __unicode__(self):
        if self.first_name or self.last_name:
            return "{0} {1}".format(self.first_name, self.last_name)
        user = self.user

        return user.username

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    # def get_organizations(self):
    #     return self.organization_set.all()

    def get_published_protocols(self, public=True, private=True):
        '''
        Returns a list of published protocols the user has access to.
        '''
        result = []

        if private:
            for org in self.user.organization_set.prefetch_related('protocol_set').all():
                result.extend( org.protocol_set.filter(published=True, public=False))

        if public:
            result.extend( Protocol.objects.filter(published=True, public=True) )

        return result

    # def get_published_org_protocols(self):
    #     '''
    #     Returns a list of published protocols the user has access to.
    #     '''
    #     result = []

    #     for org in self.user.organization_set.prefetch_related('protocol_set').all():
    #         result.extend( org.protocol_set.filter(published=True, public=False))

    #     return result

    # def get_published_public_protocols(self):
    #     '''
    #     Returns a list of public protocols the user has access to.
    #     '''
    #     return Protocol.objects.filter(published=True, public=True)

    # def get_all_published_protocols(self):
    #     '''
    #     Returns a list of all protocols the user has access to.
    #     example:
    #     user.profile.get_all_published_protocols()
    #     '''
    #     result = self.get_published_org_protocols()
    #     result.extend( self.get_published_public_protocols() )

    #     return result

    def get_all_published_protocol_choices(self):
        return [(protocol.pk, protocol.owner.name + " - " + protocol.name) for protocol in self.get_published_protocols()]


class Favorite(TimeStampedModel):
    '''For simple bookmarking by a user for quickly finding protocols they have tagged as liking'''
    user = models.ForeignKey(User, blank=True, null=True)
    protocols = models.ManyToManyField(Protocol)
    note = models.TextField(_("Notes"), blank=True, null=True)

    def __unicode__(self):
        return self.user.username + " - " + self.protocol.name
