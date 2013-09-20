from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from django.utils.log import getLogger
from django.views.generic.detail import SingleObjectMixin
from django import http
from django.core.urlresolvers import reverse
# import django.template as template

from braces.views import LoginRequiredMixin

from core.utils import check_owner_edit_authorization, check_owner_view_authorization
from protocols.models import Protocol

logger = getLogger('django.request')


# class PathGenerator(template.Node):
#     def render(self, context):
#         return "FOO"


#####################
# MIXINS
#####################

class PathMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PathMixin, self).get_context_data(**kwargs)
        context['paths'] = [{'name':"Dashboard", 'icon':'home', 'url':reverse('dashboard')}]
        return context 


#####################
# VIEWS
#####################

class DashboardView(PathMixin, LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        del(context['paths'][-1]['url'])

        context['titleBlock'] = {'prefix':str(self.request.user) + "\'s", 'title':'Dashboard', 'suffix':""}
        
        return context


class DocumentationView(TemplateView):
    template_name = "core/documentation.html"


class FAQView(TemplateView):
    template_name = "core/FAQ.html"    

class ReleaseNotes(TemplateView):
    template_name = "core/release_notes.html"        


class AuthorizedOrganizationMixin(object):
    '''Checks to see if the user has the right to see the given protocol'''

    # NEEDS TO BE UPDATE TO HANDLE NO PROTOCOL PASSED AND JUST AN ORG

    def get_protocol(self):
        if hasattr(self, "protocol"):       # IF THE ATTR IS ALREADY SET, USE THAT
            return self.protocol
            
        slug = self.kwargs.get('protocol_slug', None)

        if slug is None:                    # IF THERE IS NO SLUG PASSED, ERROR (IS THIS NEEDED?)
            print "No slug passed"
            raise Http404()

        # Is there an object attached to self?
        if hasattr(self, "object"):                         
            # If so, and it's a Protocol, then use that
            if isinstance(self.object, Protocol):
                protocol = self.object
            else:
                # Otherwise find the protocol normally
                protocol = get_object_or_404(Protocol, slug=self.kwargs.get('protocol_slug', None))
                # print "object isn't a protocol`"
        else:
            # Find the protocol normally
            protocol = get_object_or_404(Protocol, slug=self.kwargs.get('protocol_slug', None))
            # print "protocol isn't an object"

        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
                return protocol
            try:                                                                # IF THEY ARE NOT AN ADMIN OR SUPERUSER, SEE IF THEY HAVE MEMBERSHIP FOR THE PROTOCOL
                membership = self.request.user.membership_set.get(pk=protocol.owner.pk)
                return protocol
            except ObjectDoesNotExist: 
               pass

        # if published just show it.
        if protocol.published:
            return protocol

        raise Http404()

    def get_context_data(self, **kwargs):
        self.protocol = self.get_protocol()
        context = super(AuthorizedOrganizationMixin, self).get_context_data(**kwargs)
        # context['protocol'] = self.protocol
        return context


class AuthorizedOrganizationEditMixin(AuthorizedOrganizationMixin):

    def check_authorization(self):
        if self.request.user.is_superuser or self.request.user.is_staff:      # IF THEY ARE SYSTEM ADMIN THE CAN SEE THE PROTOCOL
            return True

        try:
            membership = self.request.user.membership_set.get(pk=item.owner.pk)
            if membership.role in ['a','w']:                                # ADMIN OR WRITE PERMISSIONS
                return True
        except ObjectDoesNotExist:
           pass
        
        raise Http404

        # if not check_owner_edit_authorization(self.protocol, self.request.user):
        #     raise Http404


class ConfirmationMixin(object):
    '''
    Simple view that handles a basic confirmation dialogue.  It expects a 
    form to have two buttons named "confirm" and "cancel".  If there is a 
    POST request made, either of these two objects will be called.  The 
    GET request simply presents the dialogue as a form.
    '''

    permanent = False
    cancel_url = None
    confirm_button_name = "confirm"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if self.confirm_button_name in request.POST:
            return self.confirm(request, *args, **kwargs)
        return self.cancel(request, *args, **kwargs)

    def confirm(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def cancel(self, request, *args, **kwargs):
        url = self.get_cancel_url(request, *args, **kwargs)
        if url:
            if self.permanent:
                return http.HttpResponsePermanentRedirect(url)
            else:
                return http.HttpResponseRedirect(url)
        else:
            logger.warning('Gone: %s', self.request.path,
                        extra={
                            'status_code': 410,
                            'request': self.request
                        })
            return http.HttpResponseGone()


    def get_cancel_url(self, request, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.cancel_url:
            url = self.cancel_url % kwargs
            args = self.request.META.get('QUERY_STRING', '')
            if args and self.query_string:
                url = "%s?%s" % (url, args)
            return url
        else:
            return None


class ConfirmationObjectView(ConfirmationMixin, SingleObjectMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
