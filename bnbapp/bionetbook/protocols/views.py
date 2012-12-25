from django.core.urlresolvers import reverse
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from braces.views import LoginRequiredMixin
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin

from protocols.forms import ProtocolForm, PublishForm, StepForm, ActionForm
from protocols.models import Protocol


class ProtocolDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol

    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ProtocolDetailView, self).get_context_data(**kwargs)
        context['steps'] = self.object.steps
        #context['steps'] = self.object.step_set.filter()

        return context


class ProtocolListView(ListView):

    model = Protocol

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Protocol.objects.filter()
        if self.request.user.is_authenticated():
            return Protocol.objects.filter(
                    Q(status=Protocol.STATUS_PUBLISHED) |
                    Q(owner=self.request.user)
                    )
        return Protocol.objects.filter(status=Protocol.STATUS_PUBLISHED)


class ProtocolCreateView(LoginRequiredMixin, CreateView):
    '''
    View used to create new protocols
    '''

    model = Protocol
    form_class = ProtocolForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProtocolCreateView, self).form_valid(form)

    def get_success_url(self):

        return self.object.get_absolute_url()


class ProtocolUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    model = Protocol
    form_class = ProtocolForm
    slug_url_kwarg = "protocol_slug"

    #def get_context_data(self, **kwargs):
    #    context = super(ProtocolUpdateView, self).get_context_data(**kwargs)
    #    #context['steps'] = self.object.step_set.select_related()

    #    return context


class ProtocolPublishView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, FormView):

    form_class = PublishForm
    template_name = "myapp/email_form.html"
    success_url = '/email-sent/'

    def get_success_url(self):
        protocol = self.get_protocol()
        return protocol.get_absolute_url()

    def form_valid(self, form):
        protocol = self.get_protocol()
        protocol.status = Protocol.STATUS_PUBLISHED
        protocol.save()
        messages.add_message(self.request, messages.INFO, "Your protocol is publushed.")
        return super(ProtocolPublishView, self).form_valid(form)


####################
# Component Base Classes

#class ComponentCreateViewBase(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, FormMixin, DetailView):
class ComponentCreateViewBase(AuthorizedForProtocolMixin, SingleObjectMixin, FormView):
    '''This view needs to properly create a view, set a form and process the form'''

    model = Protocol
    template_name = "steps/step_create.html"
    slug_url_kwarg = "protocol_slug"
    form_class = StepForm
    success_url = None

    def get_url_args(self):
        protocol = self.get_protocol()
        return {'protocol_slug': protocol.slug}

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            url = reverse(self.success_url, kwargs=self.get_url_args())
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def get_context_data(self, **kwargs):
        print "GET CONTEXT DATA"
        context = super(ComponentCreateViewBase, self).get_context_data(**kwargs)
        context['steps'] = self.object.steps

        if 'step_slug' in self.kwargs:
            context['step'] = self.object.components[self.kwargs['step_slug']]

        context['form'] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        print "GET CALLED"
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print "POST CALLED"

        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            print "FORM VALID"
            return self.form_valid(form)
        else:
            print "FORM INVALID"
            return self.form_invalid(form)


####################
# Step Tools

class StepListView(AuthorizedForProtocolMixin, ListView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    template_name = "steps/step_list.html"

    def get_queryset(self):     # NEEDS TO GET THIS FROM THE SLUG PASSED IN

        slug = self.kwargs.get('slug')

        #if self.request.user.is_superuser or self.request.user.is_staff:
        return Protocol.objects.filter(slug="first-strand-cdna-synthesis-oligodt")
        #if self.request.user.is_authenticated():
        #    return Protocol.objects.filter(
        #            Q(status=Protocol.STATUS_PUBLISHED) |
        #            Q(owner=self.request.user)
        #            )
        #return Protocol.objects.filter(status=Protocol.STATUS_PUBLISHED)

        #return []
        #return slug



class StepDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol
    template_name = "steps/step_detail.html"
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(StepDetailView, self).get_context_data(**kwargs)
        step_slug = self.kwargs['step_slug']
        context['step'] = self.object.components[step_slug]
        return context


class StepCreateView(ComponentCreateViewBase):
    '''Creates and appends a step to a protocol.'''

    template_name = "steps/step_create.html"
    form_class = StepForm
    success_url = 'protocol_detail'

    def form_valid(self, form):
        protocol = self.get_protocol()

        if 'steps' in protocol.data:
            protocol.data['steps'].append(form.cleaned_data)
        else:
            protocol.data['steps'] = [form.cleaned_data]
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your step was added.")
        return super(StepCreateView, self).form_valid(form)

    def form_invalid(self, form):
        protocol = self.get_protocol()
        # NEED TO SET OBJECT
        return super(StepCreateView, self).form_invalid(form)



class ActionDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol
    template_name = "actions/action_detail.html"
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ActionDetailView, self).get_context_data(**kwargs)
        action_slug = self.kwargs['action_slug']
        context['action'] = self.object.components[action_slug]
        context['step'] = context['action'].step
        return context




class ActionCreateView(ComponentCreateViewBase):

    form_class = ActionForm
    template_name = "actions/action_create.html"
    success_url = 'protocol_detail'

    #def get_context_data(self, **kwargs):
    #    context = super(ActionCreateView, self).get_context_data(**kwargs)
    #    step_slug = self.kwargs['step_slug']
    #    context['step'] = self.object.components[step_slug]
    #    context['form'] = ActionForm()
    #    return context

