from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from core.utils import check_protocol_edit_authorization
from protocols.models import Protocol


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class AuthorizedForProtocolMixin(object):

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
