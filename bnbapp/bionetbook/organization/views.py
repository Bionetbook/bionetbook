from django import forms, http
from django.http import Http404, HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView
from django.utils import simplejson

from braces.views import LoginRequiredMixin

from protocols.models import Protocol, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
from schedule.models import Calendar
from experiment.models import Experiment
from protocols.utils import VERB_CHOICES, VERB_FORM_DICT


#class OrganizationDetailView(AuthorizedOrganizationMixin, DetailView):
# class OrganizationDetailView(LoginRequiredMixin, DetailView):

#     model = Organization

    #slug_url_kwarg = "org_slug"

    #def get_context_data(self, **kwargs):
    #    context = super(ProtocolDetailView, self).get_context_data(**kwargs)
    #    context['steps'] = self.object.steps
    #    return context


#class Organization_detailView(TemplateView):
#	template_name = 'organization/organization_detail.html'


class OrganizationMainView(LoginRequiredMixin, TemplateView):
	model = Organization
	slug_url_kwarg = "owner_slug"
	template_name = "organization/organization_main.html"    
	def get_context_data(self, **kwargs):
		context = super(OrganizationMainView, self).get_context_data(**kwargs)
		slug = self.kwargs.get(self.slug_url_kwarg, None)	
		org = self.request.user.organization_set.get(slug=slug)
		viewableProtocols = [p for p in org.protocol_set.all() if p.author==self.request.user]
		publishedProtocols = [p for p in org.protocol_set.all() if p.published]
		viewableProtocols = list(set(viewableProtocols + publishedProtocols))
		workflows = [w for w in self.request.user.workflow_set.all() if w.owner==org]
		experiments = [e for e in self.request.user.experiment_set.all() if e.owner==org]
		if experiments:
			context['experiments'] = experiments
		else:
			context['experiments'] = None
		if workflows:
			context['workflows'] = workflows
		else:
			context['workflows'] = None
		if org:
			context['organization'] = org
		else:
			context['organization'] = None
		if viewableProtocols:
			context['protocols'] = viewableProtocols
		else:
			context['protocols'] = None
		return context
    
    # def get_context_data(self, **kwargs):
    #     context = super(OrganizationListView, self).get_context_data(**kwargs)
    #     context['titleBlock'] = {'title':self.object.name, 'suffix':"Protocols"}
    #     return context
