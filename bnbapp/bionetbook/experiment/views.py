# Create your views here.
from django import forms, http
from django.http import Http404, HttpResponse
from django.views.generic import ListView, View, CreateView, FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView
from django.utils import simplejson

from core.views import PathMixin
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin
from django.template.defaultfilters import slugify
from experiment.forms import ExperimentManualForm
from protocols.models import Protocol, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
from schedule.models import Calendar
from experiment.models import Experiment
from protocols.utils import VERB_CHOICES, VERB_FORM_DICT
from workflow.models import Workflow


class ExperimentDetailView(LoginRequiredMixin, TemplateView):

	model = Experiment
	slug_url_kwarg = "experiment_slug"
	template_name = "experiment/experiment_detail.html"

	def get_context_data(self, **kwargs):
		context = super(ExperimentDetailView, self).get_context_data(**kwargs)
		slug = self.kwargs.get(self.slug_url_kwarg, None)
		experiment = self.request.user.experiment_set.get(slug=slug)
		org = self.request.user.organization_set.get(slug=self.kwargs['owner_slug'])
		workflow = experiment.workflow
		if experiment:
			context['experiment'] = experiment
		else:
			context['experiment'] = None
		if workflow:
			context['workflow'] = workflow
		else:
			context['workflow'] = None
		if org:
			context['organization'] = org
		else:
			context['organization'] = None
		return context


class ExperimentCreateView(PathMixin, LoginRequiredMixin, FormView):

	model = Experiment
	form_class = ExperimentManualForm
	slug_url_kwarg = "owner_slug"
	template_name = "experiment/experiment_form.html"

	def get_success_url(self):
		return self.get_absolute_url()

	def form_valid(self, form):
		slug = self.kwargs.get(self.slug_url_kwarg, None)
		org = Organization.objects.get(slug=slug)

		e = Experiment()
		e.user = self.request.user
		e.workflow = Workflow.objects.get(pk=form.cleaned_data['workflows'][0])
		e.data = {'meta':{}}
		e.name = form.cleaned_data['name']
		e.slug = slugify(form.cleaned_data['name'])
		e.owner = org
		e.save()
		return HttpResponseRedirect(e.get_absolute_url())

	def get_form(self, form_class):
		form = form_class(**self.get_form_kwargs())
		workflows = Organization.objects.get(slug=self.kwargs['owner_slug']).workflow_set.all()
		workflows = [w for w in workflows if w.user==self.request.user]
		form.fields['workflows'] = forms.ChoiceField(
			label="Workflows",
			choices=((x.pk,x) for x in workflows))
		return form

