#from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django import http
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
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView

from workflow.models import Workflow
from protocols.models import Protocol 	#, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
from workflow.forms import WorkflowForm

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


# class WorkflowCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
#     '''This view needs to properly create a view, set a form and process the form'''

#     model = Workflow
#     slug_url_kwarg = "owner_slug"
#     form_class = WorkflowForm


class WorkflowCreateView(LoginRequiredMixin, CreateView):
    '''
    View used to create new protocols
    '''

    model = Workflow
    form_class = WorkflowForm
    slug_url_kwarg = "owner_slug"

    #def get_queryset(self):
    #slug = self.kwargs.get(self.slug_url_kwarg, None)

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super(ProtocolCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        org = Organization.objects.get(slug=slug)

        form.instance.owner = org
        form.instance.author = self.request.user

        return super(WorkflowCreateView, self).form_valid(form)


    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = form_class(**self.get_form_kwargs())
        form.instance.author = self.request.user
        #form.fields['owner'].choices = [(org.pk, org.name) for org in self.request.user.organization_set.all()]
        # NEED TO CHANGE THE FORM CLASS'S QUERYSET ON THE FIELD
        return form


class WorkflowUpdateView(LoginRequiredMixin, UpdateView):
    #pass
    #slugs = []
    #node_type = None
    model = Workflow
    slug_url_kwarg = "owner_slug"
    form_class = WorkflowForm


class WorkflowDeleteView(LoginRequiredMixin, ConfirmationObjectView):

    model = Workflow
    slug_url_kwarg = "workflow_slug"
    template_name = "workflow/workflow_delete.html"
    success_url = "workflow_list"

    def get_cancel_url(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.object.get_absolute_url()

    def get_url_args(self):
        args = {'owner_slug':self.object.owner.slug}
        return args

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        url = reverse(self.success_url, kwargs=self.get_url_args())
        message = "The Workflow \"%s\" was deleted." % self.object.name
    #     self.object.delete()
        messages.add_message(self.request, messages.INFO, message)
        return http.HttpResponseRedirect(url)
