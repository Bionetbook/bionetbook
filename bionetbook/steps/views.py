from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from braces.views import LoginRequiredMixin

from protocols.models import Protocol
from steps.forms import StepForm
from steps.models import Step


class StepBaseView(object):

    def get_protocol(self):
        return get_object_or_404(Protocol, slug=self.kwargs.get('protocol_slug', None))

    def get_breadcrumbs(self):
        protocol = getattr(self, "protocol", self.get_protocol())
        return [
                                (reverse("protocol_list"), "protocols"),
                                (protocol.get_absolute_url(), protocol),
                                (reverse("step_list", kwargs={'protocol_slug': protocol.slug}), "steps"),
                                ]

    def get_context_data(self, **kwargs):
        context = super(StepBaseView, self).get_context_data(**kwargs)
        self.protocol = self.get_protocol()

        context['protocol'] = self.protocol
        context['breadcrumbs'] = self.get_breadcrumbs()

        return context


class StepDetailView(StepBaseView, DetailView):

    model = Step

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)
        context['breadcrumbs'].append((self.object.get_absolute_url(), self.object.name), )
        context['actions'] = self.object.action_set.select_related()

        return context


class StepListView(StepBaseView, ListView):

    model = Step


class StepCreateView(LoginRequiredMixin, StepBaseView, CreateView):

    model = Step
    form_class = StepForm

    def form_valid(self, form):
        form.instance.protocol = self.get_protocol()
        return super(StepCreateView, self).form_valid(form)

    def get_success_url(self):

        return self.object.get_absolute_url()


class StepUpdateView(LoginRequiredMixin, StepBaseView, UpdateView):

    model = Step
    form_class = StepForm

    def get_context_data(self, **kwargs):
        context = super(StepUpdateView, self).get_context_data(**kwargs)

        return context
