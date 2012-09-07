from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from braces.views import LoginRequiredMixin

from actions.forms import ActionForm
from actions.models import Action
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin
from steps.models import Step
from verbs.views import VerbBaseView


class ActionBaseView(AuthorizedForProtocolMixin):

    def get_step(self):
        return get_object_or_404(Step, slug=self.kwargs.get('step_slug', None))

    def get_breadcrumbs(self):
        step = getattr(self, "step", self.get_step())
        return [
                                (reverse("protocol_list"), "protocols"),
                                (self.protocol.get_absolute_url(), self.protocol),
                                (reverse("step_list", kwargs={'protocol_slug': self.protocol.slug}), "steps"),
                                (reverse("step_detail", kwargs=dict(protocol_slug=self.protocol.slug, slug=step.slug)), step.name),
                                (reverse("action_list", kwargs=dict(protocol_slug=self.protocol.slug, step_slug=step.slug)), "actions"),
                                ]

    def get_context_data(self, **kwargs):
        context = super(ActionBaseView, self).get_context_data(**kwargs)
        self.step = self.get_step()

        context['step'] = self.step
        context['breadcrumbs'] = self.get_breadcrumbs()

        return context


class ActionDetailView(ActionBaseView, DetailView):

    model = Action

    def get_context_data(self, **kwargs):
        context = super(ActionDetailView, self).get_context_data(**kwargs)
        context['breadcrumbs'].append((self.object.get_absolute_url(), self.object.name), )

        return context


class ActionListView(ActionBaseView, ListView):

    model = Action


class ActionCreateView(LoginRequiredMixin, ActionBaseView, AuthorizedforProtocolEditMixin, VerbBaseView, CreateView):

    model = Action
    form_class = ActionForm

    def form_valid(self, form):
        self.protocol = self.get_protocol()
        form.instance.step = self.get_step()
        verb_form_base = self.get_verb_form(self.request.POST.get("verb_slug", None))
        verb_form = verb_form_base(self.request.POST)
        if verb_form.is_valid():
            form.instance.verb_attributes = verb_form.cleaned_data
        return super(ActionCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ActionUpdateView(LoginRequiredMixin, ActionBaseView, AuthorizedforProtocolEditMixin, VerbBaseView, UpdateView):

    model = Action
    form_class = ActionForm

    def form_valid(self, form):
        verb_form_base = self.get_verb_form(self.request.POST.get("verb_slug", None))
        verb_form = verb_form_base(self.request.POST)
        if verb_form.is_valid():
            form.instance.verb_attributes = verb_form.cleaned_data
        return super(ActionUpdateView, self).form_valid(form)


class ActionVerbAjaxView(LoginRequiredMixin, VerbBaseView, TemplateView):

    template_name = "actions/action_verb_ajax.html"

    def get_context_data(self, **kwargs):
        context = super(ActionVerbAjaxView, self).get_context_data(**kwargs)
        verb_form_base = self.get_verb_form(slug=self.kwargs.get("verb_slug", None))
        try:
            action = Action.objects.get(pk=self.kwargs.get("action_pk", None))
            context['form'] = verb_form_base(initial=action.verb_attributes)
        except Action.DoesNotExist:
            context['form'] = verb_form_base()

        return context
