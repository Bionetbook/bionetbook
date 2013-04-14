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

from workflow.models import Workflow
from protocols.models import Protocol 	#, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization

# Workflow Views
class WorkflowDetailView(LoginRequiredMixin, DetailView):

    model = Workflow
    slug_url_kwarg = "workflow_slug"


class WorkflowListView(LoginRequiredMixin, ListView):

    model = Organization
    slug_url_kwarg = "owner_slug"
    context_object_name = "workflow_list"

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



class WorkflowCreateViewBase(LoginRequiredMixin, AuthorizedForProtocolMixin, SingleObjectMixin, FormView):
    '''This view needs to properly create a view, set a form and process the form'''

    model = Workflow


class WorkflowUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    slugs = []
    #node_type = None


class WorkflowDeleteView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, ConfirmationObjectView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
