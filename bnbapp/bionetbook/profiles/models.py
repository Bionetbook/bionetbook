from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import EmptyQuerySet

from django_extensions.db.models import TimeStampedModel

from protocols.models import Protocol
from organization.models import Organization

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
    orgs = models.CharField( max_length=100, null=True, blank=True)

    def __unicode__(self):
        if self.first_name or self.last_name:
            return "{0} {1}".format(self.first_name, self.last_name)
        user = self.user

        return user.username

    def save(self, *args, **kwargs):
        self.update_orgs()                              # Update the cache list of organizations whenever profile is saved
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    # def get_organizations(self):
    #     return self.organization_set.all()

    def get_accessable_protocols(self):
        draft = self.get_private_draft_protocols()
        private = self.get_private_protocols()
        public = self.get_public_protocols()

        return list(draft) + list(private) + list(public)

        # return draft + private + public

    def get_published_protocols(self, public=True, private=True):
        '''
        Returns a list of published protocols the user has access to.
        '''
        return list( self.get_published_protocols_qs(public, private) )

    def get_published_protocols_qs(self, public=True, private=True):
        '''
        Returns a list of published protocols the user has access to.
        '''
        result = None

        if private:
            for org in self.user.organization_set.prefetch_related('protocol_set').all():
                if result:
                    result = result | org.protocol_set.filter(published=True, public=False)
                else:
                    result = org.protocol_set.filter(published=True, public=False)

        if public:
            if result:
                result = result | Protocol.objects.filter(published=True, public=True)
            else:
                result = Protocol.objects.filter(published=True, public=True)

        return result


    def can_read_protocol(self, pid=None, slug=None):
        '''Returns None if it can not read the protocol, the protocol object if they can'''

        result = None
        if pid:
            protocols = Protocol.objects.filter(pk=pid, owner_id__in=u.organization_set.values_list('id', flat=True))
        elif slug:
            protocols = Protocol.objects.filter(slug=slug, owner_id__in=u.organization_set.values_list('id', flat=True))

        if protocols:
            result = protocols[0]

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

    def get_private_draft_protocols(self):
        # return self.get_published_protocols()
        return Protocol.objects.filter(owner__in=self.user.organization_set.all(), published=False, public=False, author=self.user)

            # context['events'] = Event.objects.filter( project__in=Project.objects.filter( org__in=self.request.user.organization_set.all() ) ).exclude( eventType="LOG" )

    def get_public_protocols(self):
        return Protocol.objects.filter(published=True, public=True)
        # return self.get_published_protocols()

    def get_private_protocols(self):
        return self.get_published_protocols(public=False)

    #**************
    # Organization Caching
    
    @property
    def org_list(self):
        return [int(x) for x in self.orgs.split(",")]

    def update_orgs(self):
        self.orgs = ",".join([str(x.id) for x in self.user.organization_set.all().order_by("id")])


class Favorite(TimeStampedModel):
    '''For simple bookmarking by a user for quickly finding protocols they have tagged as liking'''
    user = models.ForeignKey(User, blank=True, null=True)
    protocols = models.ManyToManyField(Protocol)
    note = models.TextField(_("Notes"), blank=True, null=True)

    def __unicode__(self):
        return self.user.username + " - " + self.protocol.name
