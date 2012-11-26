from django import forms
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView

from braces.views import LoginRequiredMixin
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin

from protocols.forms import ProtocolForm, PublishForm
from protocols.models import Protocol


class ProtocolDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol

    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ProtocolDetailView, self).get_context_data(**kwargs)
        context['steps'] = self.object.step_set.filter()

        return context


class ProtocolListView(ListView):

    model = Protocol

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Protocol.objects.filter()
        if self.request.user.is_authenticated():
            return Protocol.objects.filter(
                    Q(status=Protocol.STATUS_PUBLISHED) |
                    Q(owner=self.request.user)
                    )
        return Protocol.objects.filter(status=Protocol.STATUS_PUBLISHED)


class ProtocolCreateView(LoginRequiredMixin, CreateView):

    model = Protocol
    form_class = ProtocolForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProtocolCreateView, self).form_valid(form)

    def get_success_url(self):

        return self.object.get_absolute_url()


class ProtocolUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    model = Protocol
    form_class = ProtocolForm
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ProtocolUpdateView, self).get_context_data(**kwargs)
        context['steps'] = self.object.step_set.select_related()

        return context


class ProtocolPublishView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, FormView):

    form_class = PublishForm
    template_name = "myapp/email_form.html"
    success_url = '/email-sent/'

    def get_success_url(self):
        protocol = self.get_protocol()
        return protocol.get_absolute_url()

    def form_valid(self, form):
        protocol = self.get_protocol()
        protocol.status = Protocol.STATUS_PUBLISHED
        protocol.save()
        messages.add_message(self.request, messages.INFO, "Your protocol is publushed.")
        return super(ProtocolPublishView, self).form_valid(form)


