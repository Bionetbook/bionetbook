from django.core.urlresolvers import reverse
#from django import forms
#from django.contrib import messages
#from django.db.models import Q
from django.views.generic import ListView, DetailView 			#, CreateView, UpdateView, FormView
#from django.views.generic.detail import SingleObjectMixin
#from django.views.generic.edit import FormMixin
#from django.http import HttpResponseRedirect


#from braces.views import LoginRequiredMixin
#from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin
from braces.views import LoginRequiredMixin

#from protocols.forms import ProtocolForm, PublishForm, StepForm, ActionForm
#from protocols.models import Protocol, Step, Action

#from protocols.utils import VERB_CHOICES, VERB_FORM_DICT
from organization.models import Organization


#class OrganizationDetailView(AuthorizedForProtocolMixin, DetailView):
class OrganizationDetailView(LoginRequiredMixin, DetailView):

    model = Organization

    #slug_url_kwarg = "org_slug"

    #def get_context_data(self, **kwargs):
    #    context = super(ProtocolDetailView, self).get_context_data(**kwargs)
    #    context['steps'] = self.object.steps
    #    return context


#class Organization_detailView(TemplateView):
#	template_name = 'organization/organization_detail.html'


class OrganizationListView(LoginRequiredMixin, ListView):

    model = Organization
