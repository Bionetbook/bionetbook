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
from workflow.forms import WorkflowForm, WorkflowManualForm
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
		if experiment:
			context['experiment'] = experiment
		else:
			context['experiment'] = None
		if org:
			context['organization'] = org
		else:
			context['organization'] = None
		return context