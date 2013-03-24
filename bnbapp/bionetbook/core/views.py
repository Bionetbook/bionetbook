from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from django.utils.log import getLogger
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin

from core.utils import check_protocol_edit_authorization
from protocols.models import Protocol

logger = getLogger('django.request')


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class AuthorizedForProtocolMixin(object):
    '''Checks to see if the user has the right to see the given protocol'''

    def get_protocol(self):
        if hasattr(self, "protocol"):
            return self.protocol
        slug = self.kwargs.get('protocol_slug', None)
        if slug is None:
            raise Http404()

        # Is there an object attached to self?
        if hasattr(self, "object"):
            # If so, and it's a Protocol, then use that
            if isinstance(self.object, Protocol):
                protocol = self.object
            else:
                # Otherwise find the protocol normally
                protocol = get_object_or_404(Protocol, slug=self.kwargs.get('protocol_slug', None))
        else:
            # Find the protocol normall
            protocol = get_object_or_404(Protocol, slug=self.kwargs.get('protocol_slug', None))

        # If superuser, staff, or owner show it
        if self.request.user.is_authenticated:
            if check_protocol_edit_authorization(protocol, self.request.user):
                return protocol

        # if published just show it.
        if protocol.published:
            return protocol

        # unpublished and not authenticated or part of the org that owns it.
        raise Http404()

    def get_context_data(self, **kwargs):
        self.protocol = self.get_protocol()
        context = super(AuthorizedForProtocolMixin, self).get_context_data(**kwargs)
        context['protocol'] = self.protocol
        context['protocol_edit_authorization'] = check_protocol_edit_authorization(self.protocol, self.request.user)
        return context


class AuthorizedforProtocolEditMixin(object):

    def check_authorization(self):
        if not check_protocol_edit_authorization(self.protocol, self.request.user):
            raise Http404

    def get_context_data(self, **kwargs):
        self.check_authorization()
        return super(AuthorizedforProtocolEditMixin, self).get_context_data(**kwargs)


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
