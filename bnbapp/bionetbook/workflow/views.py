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

# Workflow Views
class WorkflowDetailView(LoginRequiredMixin, TemplateView):

    model = Workflow
    slug_url_kwarg = "workflow_slug"
    template_name = "workflow/workflow_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WorkflowDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        workflow = self.request.user.workflow_set.get(slug=slug)
        org = self.request.user.organization_set.get(slug=self.kwargs['owner_slug'])
        if workflow:
            context['workflow'] = workflow
        else:
            context['workflow'] = None
        if org:
            context['organization'] = org
        else:
            context['organization'] = None
            print "NONE"
        protocols = [Protocol.objects.get(pk=p) for p in workflow.data['protocols']]
        context['protocols'] = protocols
        return context


class WorkflowListView(LoginRequiredMixin, ListView):

    model = Workflow
    slug_url_kwarg = "owner_slug"
    # context_object_name = "workflow_list"

    # def get_queryset(self):
    #     """
    #     Get the list of items for this view. This must be an iterable, and may
    #     be a queryset (in which qs-specific behavior will be enabled).
    #     """

    #     slug = self.kwargs.get(self.slug_url_kwarg, None)

    #     if self.queryset is not None:
    #         queryset = self.queryset
    #         if hasattr(queryset, '_clone'):
    #             queryset = queryset._clone()
    #     elif self.model is not None and slug:
    #         self.object = self.model.objects.get(slug=slug)
    #         queryset = self.object.workflow_set.all()
    #     else:
    #         raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'" % self.__class__.__name__)
    #     return queryset


    def get_context_data(self, **kwargs):
        context = super(WorkflowListView, self).get_context_data(**kwargs)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        workflow = self.request.user.workflow_set.get(slug=slug)
        if workflow:
            context['workflow'] = workflow
        else:
            context['workflow'] = None
        return context


# class WorkflowCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
#     '''This view needs to properly create a view, set a form and process the form'''

#     model = Workflow
#     slug_url_kwarg = "owner_slug"
#     form_class = WorkflowForm


class WorkflowCreateView(PathMixin, LoginRequiredMixin, FormView):
    '''
    View used to create new protocols
    '''

    model = Workflow
    form_class = WorkflowManualForm
    slug_url_kwarg = "owner_slug"
    template_name = "workflow/workflow_form.html"

    #def get_queryset(self):
    #slug = self.kwargs.get(self.slug_url_kwarg, None)

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super(ProtocolCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.get_absolute_url()


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        org = Organization.objects.get(slug=slug)

        # form.instance.owner = org
        # form.instance.user = self.request.user
        w = Workflow()
        w.name = form.cleaned_data['name']
        w.user = self.request.user
        w.data = {'meta':{}, 'protocols':form.cleaned_data['protocols']}
        w.slug = slugify(form.cleaned_data['name'])
        w.owner = org
        w.save()
        return HttpResponseRedirect(w.get_absolute_url())

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = form_class(**self.get_form_kwargs())
        protocols = Organization.objects.get(slug=self.kwargs['owner_slug']).protocol_set.all()
        protocols = [p for p in protocols if p.author==self.request.user or p.published]
        form.fields['protocols'] = forms.MultipleChoiceField(
            label="Protocols",
            choices=((x.pk,x) for x in protocols),
            widget=forms.CheckboxSelectMultiple())
        #form.fields['organization'] = Organization.objects.get(slug=self.kwargs['owner_slug'])
        #form.fields['owner'].choices = [(org.pk, org.name) for org in self.request.user.organization_set.all()]
        # NEED TO CHANGE THE FORM CLASS'S QUERYSET ON THE FIELD
        return form


# class WorkflowUpdateView(LoginRequiredMixin, UpdateView):
#     #pass
#     #slugs = []
#     #node_type = None
#     model = Workflow
#     slug_url_kwarg = "workflow_slug"
#     form_class = WorkflowForm


# class WorkflowDeleteView(LoginRequiredMixin, ConfirmationObjectView):

#     model = Workflow
#     slug_url_kwarg = "workflow_slug"
#     template_name = "workflow/workflow_delete.html"
#     success_url = "workflow_list"

#     def get_cancel_url(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return self.object.get_absolute_url()

#     def get_url_args(self):
#         args = {'owner_slug':self.object.owner.slug}
#         return args

#     def confirm(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         url = reverse(self.success_url, kwargs=self.get_url_args())
#         message = "The Workflow \"%s\" was deleted." % self.object.name
#     #     self.object.delete()
#         messages.add_message(self.request, messages.INFO, message)
#         return http.HttpResponseRedirect(url)
