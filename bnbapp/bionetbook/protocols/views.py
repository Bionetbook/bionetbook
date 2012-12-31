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
from protocols.models import Protocol, Step, Action

from protocols.utils import VERB_CHOICES, VERB_FORM_DICT


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
    form_prefix = None

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

        for key in ['step_slug', 'action_slug']:
            if key in self.kwargs:
                ctx_key = key.split('_')[0]
                context[ctx_key] = self.object.components[self.kwargs[key]]

        context['verb_slug'] = self.kwargs['verb_slug']
        context['form'] = self.form_class(prefix=self.form_prefix)  #Set the prefix on the form
        return context

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        #print "POST CALLED"

        self.object = self.get_object()

        form_class = self.get_form_class(prefix=self.form_prefix)
        form = self.get_form(form_class)

        if form.is_valid():
            print "FORM VALID"
            return self.form_valid(form)
        else:
            print "FORM INVALID"
            return self.form_invalid(form)


####################
# Step Tools

"""
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
"""


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
        new_step = Step(protocol, data=form.cleaned_data)

        if 'steps' in protocol.data:
            protocol.data['steps'].append(new_step)
        else:
            protocol.data['steps'] = [new_step]
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your step was added.")
        return super(StepCreateView, self).form_valid(form)

    def form_invalid(self, form):
        protocol = self.get_protocol()
        return super(StepCreateView, self).form_invalid(form)


class ActionDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol
    template_name = "actions/action_detail.html"
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ActionDetailView, self).get_context_data(**kwargs)
        action_slug = self.kwargs['action_slug']
        context['action'] = self.object.components[action_slug]
        context['step'] = context['action'].step       #NOT SURE IF THIS IS BETTER THEN THE ABOVE TECHNIQUE
        return context


class ActionVerbListView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol
    template_name = "actions/action_verb_list.html"
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        print "ACTION VERB LIST"
        context = super(ActionVerbListView, self).get_context_data(**kwargs)
        step_slug = self.kwargs['step_slug']
        context['step'] = self.object.components[step_slug]
        context['verbs'] = VERB_CHOICES
        return context


class ActionCreateView(ComponentCreateViewBase):

    form_class = ActionForm # THIS WILL ONLY COVER ONE OF TWO FORMS
    template_name = "actions/action_create.html"
    success_url = 'step_detail'
    form_prefix = 'action'

    def get_url_args(self):
        protocol = self.get_protocol()
        context = self.get_context_data()
        return {'protocol_slug': protocol.slug, 'step_slug':context['step'].slug}


    def get_context_data(self, **kwargs):
        '''Ads the Verb form to the context'''
        context = super(ActionCreateView, self).get_context_data(**kwargs)

        verb_slug = context['verb_slug']
        if not 'verb_form' in kwargs:
            context['verb_form'] = VERB_FORM_DICT[verb_slug](prefix='verb')
            context['verb_name'] = context['verb_form'].name
        return context


    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''

        self.object = self.get_object()
        args = self.get_form_kwargs()
        #ctx = self.get_context_data()
        #ctx['object'] = self.get_protocol()

        # POPULATE FORMS
        #form_class = self.get_form_class()
        #form = self.get_form(form_class, prefix=self.form_prefix)
        #form = form_class(args, prefix=self.form_prefix) 
        # NEED TO GET VERB FORM HERE

        form = ActionForm(request.POST, prefix='action')
        verb_slug = self.kwargs.get('verb_slug', None)
        verb_form = VERB_FORM_DICT[verb_slug](request.POST, prefix='verb')

        if form.is_valid() and verb_form.is_valid():
            print "FORM VALID"
            return self.form_valid(form, verb_form)
        else:
            print "FORM INVALID"
            return self.form_invalid(form, verb_form)


    def form_invalid(self, form, verb_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        #ctx = self.get_context_data(object=self.object, form=form, verb_form=verb_form)
        ctx = self.get_context_data(object=self.object)
        ctx['form'] = form
        ctx['verb_form'] = verb_form
        # FORMS NOT PASSING POPULATED
        return self.render_to_response(ctx)


    def form_valid(self, form, verb_form):
        '''Takes in two forms for processing'''
        protocol = self.get_protocol()
        context = self.get_context_data()
        step = context['step']

        # COMBINE THE DATA FROM THE TWO FORMS
        new_data = dict(form.cleaned_data.items() + verb_form.cleaned_data.items())
        new_action = Action(protocol, step=step, data=new_data)

        if 'actions' in step:
            step['actions'].append(new_action)
        else:
            step['actions'] = [new_action]
        #protocol.save()

        messages.add_message(self.request, messages.INFO, "Your action was added.")
        return super(ActionCreateView, self).form_valid(form)

    #def get_context_data(self, **kwargs):
    #    context = super(ActionCreateView, self).get_context_data(**kwargs)
    #    step_slug = self.kwargs['step_slug']
    #    context['step'] = self.object.components[step_slug]
    #    context['form'] = ActionForm()
    #    return context

