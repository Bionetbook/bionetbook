# Create your views here.
from django import forms, http
from django.http import Http404, HttpResponse
from django.views.generic import ListView, View, CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from core.views import ConfirmationObjectView
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


class ExperimentSetupMixin(PathMixin):
	pathEnd = {}
	titleMarks = {'suffix':"",'prefix':""}

	def get_context_data(self, **kwargs):
		context = super(ExperimentSetupMixin, self).get_context_data(**kwargs)
		experiment_slug = self.kwargs.get('experiment_slug', None)

		prefix = self.titleMarks['prefix']
		suffix = self.titleMarks['suffix']
		title = ""

		if experiment_slug:
			context['experiment'] = self.request.user.experiment_set.get(slug=experiment_slug)
			context['organization'] = context['experiment'].owner
			context['workflow'] = context['experiment'].workflow
		else:
			owner_slug = self.kwargs.get('owner_slug', None)
			if owner_slug:
				context['organization'] = self.request.user.organization_set.get(slug=owner_slug)

		if 'organization' in context:
			context['paths'].append({'name':context['organization'].name, 'url':context['organization'].get_absolute_url()})
			title = context['organization'].name

			if 'experiment' in context:
				context['paths'].append({'name':context['experiment'].name, 'url':context['experiment'].get_absolute_url()})
				prefix = title
				title = context['experiment'].name

		if self.pathEnd:
			context['paths'].append( self.pathEnd )
			suffix = self.pathEnd['name']
		else:
			del(context['paths'][-1]['url'])

		if title:
			context['titleBlock'] = {'prefix':prefix, 'title':title, 'suffix':suffix}
		return context


class ExperimentDetailView(ExperimentSetupMixin, LoginRequiredMixin, TemplateView):

	model = Experiment
	slug_url_kwarg = "experiment_slug"
	template_name = "experiment/experiment_detail.html"

	def get_context_data(self, **kwargs):
		context = super(ExperimentDetailView, self).get_context_data(**kwargs)
		return context


class ExperimentUpdateView(ExperimentSetupMixin, LoginRequiredMixin, FormView):
	model = Experiment
	form_class = ExperimentManualForm
	slug_url_kwarg = "owner_slug"
	template_name = "experiment/experiment_form.html"
	pathEnd = {'name':'Edit'}


	def form_valid(self, form):
		slug = self.kwargs.get(self.slug_url_kwarg, None)
		org = self.request.user.organization_set.get(slug=slug)
		slug = self.kwargs.get('experiment_slug', None)
		exp = self.request.user.experiment_set.get(slug=slug)

		exp.workflow = self.request.user.workflow_set.get(pk=form.cleaned_data['workflows'][0])
		exp.name = form.cleaned_data['name']
		exp.slug = slugify(exp.name)
		exp.save()
		return HttpResponseRedirect(exp.get_absolute_url())

	def get_form(self, form_class):
		form = form_class(**self.get_form_kwargs())
		try:
			exp = self.request.user.experiment_set.get(slug=self.kwargs['experiment_slug'])
			org = self.request.user.organization_set.get(slug=self.kwargs['owner_slug'])
			workflows = org.workflow_set.all()
			workflows = [w for w in workflows if w.user==self.request.user and w!=exp.workflow]
			workflows.insert(0,exp.workflow)
			form.initial['name'] = exp.name
			form.fields['workflows'] = forms.ChoiceField(
				label="Workflows",
				choices=((x.pk,x) for x in workflows))
			return form
		except:
			# try:
			# 	org = self.request.user.organization_set.get(slug=self.kwargs['owner_slug'])
			# 	workflows = org.workflow_set.all()
			# 	workflows = [w for w in workflows if w.user==self.request.user]
			# 	form.fields['workflows'] = forms.ChoiceField(
			# 		label="Workflows",
			# 		choices=((x.pk,x) for x in workflows))
			# except:
			# 	raise Http404
			# return form
			raise Http404


	# def post(self, request, *args, **kwargs):
	# 	'''This is done to handle the two forms'''
	# 	form = self.form_class(request.POST)

	# 	if form.is_valid():
	# 		return self.form_valid(form)
	# 	else:
	# 		return self.form_invalid(form)

	# def form_invalid(self, form):
	# 	return self.render_to_response(self.get_context_data(form=form))

class ExperimentCreateView(ExperimentSetupMixin, LoginRequiredMixin, FormView):

	model = Experiment
	form_class = ExperimentManualForm
	slug_url_kwarg = "owner_slug"
	template_name = "experiment/experiment_form.html"
	pathEnd = {'name':'New Experiment'}

	def get_success_url(self):
		return self.get_absolute_url()

	def form_valid(self, form):
		slug = self.kwargs.get(self.slug_url_kwarg, None)
		org = self.request.user.organization_set.get(slug=slug)

		e = Experiment()
		e.user = self.request.user
		e.workflow = self.request.user.workflow_set.get(pk=form.cleaned_data['workflows'][0])
		e.data = {'meta':{}}
		e.name = form.cleaned_data['name']
		e.slug = slugify(form.cleaned_data['name'])
		e.owner = org
		e.save()
		for cal in self.request.user.calendar_set.all():
			cal.addExperiment(e)
		return HttpResponseRedirect(e.get_absolute_url())

	def get_form(self, form_class):
		form = form_class(**self.get_form_kwargs())
		try:
			org = self.request.user.organization_set.get(slug=self.kwargs['owner_slug'])
			workflows = org.workflow_set.all()
			workflows = [w for w in workflows if w.user==self.request.user]
			form.fields['workflows'] = forms.ChoiceField(
				label="Workflows",
				choices=((x.pk,x) for x in workflows))
		except:
			raise Http404
		return form

