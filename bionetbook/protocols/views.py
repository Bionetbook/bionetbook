from django.views.generic import ListView, DetailView, CreateView, UpdateView

from braces.views import LoginRequiredMixin
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin

from protocols.forms import ProtocolForm
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
