#from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.urlresolvers import reverse
#from django import forms, http
from django.http import Http404
from django.contrib import messages
#from django.db.models import Q
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
#from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
#from django.views.generic.edit import FormMixin
#from django.http import HttpResponseRedirect
#from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, ConfirmationObjectView

#from protocols.forms import ProtocolPublishForm, StepForm, ActionForm, ComponentForm, MachineForm, ThermocyclerForm, OrganizationListForm
#from protocols.forms.baseforms import ProtocolForm
from workflow.models import Workflow
from protocols.models import Protocol 	#, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization

#from protocols.utils import VERB_CHOICES, VERB_FORM_DICT

# Workflow View

class WorkflowDetailView(LoginRequiredMixin, AuthorizedForProtocolMixin, DetailView):

    model = Workflow
    slug_url_kwarg = "workflow_slug"
    #slugs = []

    # def get_context_data(self, **kwargs):

    #     context = super(WorkflowDetailView, self).get_context_data(**kwargs)

    #     for slug in self.slugs:
    #         objectid = self.kwargs[slug]
    #         if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF
    #             slug = slug[:-5]
    #         context[slug] = self.object.nodes[objectid]

    #     return context

#class WorkflowListView(LoginRequiredMixin, AuthorizedForProtocolMixin, ListView):
class WorkflowListView(LoginRequiredMixin, ListView):

    model = Organization
    slug_url_kwarg = "owner_slug"
    context_object_name = "workflow_list"
    #template_name = "protocols/protocol_list.html"

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """

        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None and slug:
            self.object = self.model.objects.get(slug=slug)
            queryset = self.object.workflow_set.all()
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'" % self.__class__.__name__)
        return queryset


    def get_context_data(self, **kwargs):
        context = super(WorkflowListView, self).get_context_data(**kwargs)
        context['organization'] = self.object
        return context


    # model = Organization
    # template_name = "protocols/protocol_list.html"
    # slug_url_kwarg = "owner_slug"

    # def get_queryset(self):
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)

    #     if slug:
    #         return Organization.objects.filter(slug=slug)
    #     else:
    #         if self.request.user.is_superuser or self.request.user.is_staff:
    #             return Organization.objects.all()    # GET ALL THE PROTOCOLS
    #         if self.request.user.is_authenticated():
    #             #return self.request.user.organizations.protocols
    #             # return Protocol.objects.filter(
    #             #         Q(status=Protocol.STATUS_PUBLISHED) |
    #             #         Q(owner=self.request.user)
    #             #         )
    #             return self.request.user.organization_set.all() # GET ALL THE ORGANIZATIONS THE USER IS A MEMEBER OF
    #         return []

    # def get_context_data(self, **kwargs):
    #     print "GETTING CONTEXT DATA"
    #     return super(WorkflowListView, self).get_context_data(**kwargs)



class WorkflowCreateViewBase(LoginRequiredMixin, AuthorizedForProtocolMixin, SingleObjectMixin, FormView):
    '''This view needs to properly create a view, set a form and process the form'''

    model = Workflow


class WorkflowUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    slugs = []
    #node_type = None


class WorkflowDeleteView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, ConfirmationObjectView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
