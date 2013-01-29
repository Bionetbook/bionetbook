from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django import forms
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin
from core.views import AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin

from protocols.forms import ProtocolForm, PublishForm, StepForm, ActionForm
from protocols.models import Protocol, Step, Action
from organization.models import Organization

from protocols.utils import VERB_CHOICES, VERB_FORM_DICT


class ProtocolDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol

    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ProtocolDetailView, self).get_context_data(**kwargs)
        context['steps'] = self.object.steps
        return context


class ProtocolListView(ListView):

    model = Organization

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Organization.objects.all()    # GET ALL THE PROTOCOLS
        if self.request.user.is_authenticated():
            #return self.request.user.organizations.protocols
            # return Protocol.objects.filter(
            #         Q(status=Protocol.STATUS_PUBLISHED) |
            #         Q(owner=self.request.user)
            #         )
            return self.request.user.organization_set.all()
        #return Protocol.objects.filter(status=Protocol.STATUS_PUBLISHED)
        #return Protocol.objects.filter(published=True)
        return []


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

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = form_class(**self.get_form_kwargs())
        form.fields['owner'].choices = [(org.pk, org.name) for org in self.request.user.organization_set.all()]
        # NEED TO CHANGE THE FORM CLASS'S QUERYSET ON THE FIELD
        return form


class ProtocolUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    model = Protocol
    form_class = ProtocolForm
    slug_url_kwarg = "protocol_slug"

    # NEED TO ONLY RETURN A PROTOCOL WHO'S PUBLISH IS SET TO False

    def get_context_data(self, **kwargs):
        context = super(ProtocolUpdateView, self).get_context_data(**kwargs)
        context['steps'] = self.object.steps
        return context

    #def form_valid(self, form):
    #    protocol = self.get_protocol()
    #    protocol.status = Protocol.STATUS_PUBLISHED
    #    protocol.save()
    #    messages.add_message(self.request, messages.INFO, "Your protocol is publushed.")
    #    return super(ProtocolPublishView, self).form_valid(form)


    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        queryset = queryset.filter(published=False)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    # def get_queryset(self):
    #     """
    #     Get the queryset to look an object up against. May not be called if
    #     `get_object` is overridden.
    #     """
    #     if self.queryset is None:
    #         if self.model:
    #             return self.model._default_manager.all()
    #         else:
    #             raise ImproperlyConfigured("%(cls)s is missing a queryset. Define "
    #                                        "%(cls)s.model, %(cls)s.queryset, or override "
    #                                        "%(cls)s.get_queryset()." % {
    #                                             'cls': self.__class__.__name__
    #                                     })
    #     return self.queryset._clone().filter(published=False)


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

        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object

        for key in ['step_slug', 'action_slug']:
            if key in self.kwargs:
                ctx_key = key.split('_')[0]
                context[ctx_key] = self.object.nodes[self.kwargs[key]]

        if 'verb_slug' in self.kwargs:
            context['verb_slug'] = self.kwargs['verb_slug']

        if not 'form' in context:
            context['form'] = self.form_class(prefix=self.form_prefix)  #Set the prefix on the form
            
        return context

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.form_prefix:
            form_class = self.get_form_class(prefix=self.form_prefix)
        else:
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
        context['step'] = self.object.nodes[step_slug]
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
            print "HAS DATA"
            protocol.data['steps'].append(new_step)
        else:
            print "CREATING DATA"
            protocol.data['steps'] = [new_step]
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your step was added.")
        return super(StepCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

'''
    def get_context_data(self, **kwargs):
        """
        If an object has been supplied, inject it into the context with the
        supplied context_object_name name.
        """
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super(StepCreateView, self).get_context_data(**context)
'''

class ComponentUpdateViewBase(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):
    pass


class StepUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):
    model = Protocol
    form_class = StepForm
    slug_url_kwarg = "protocol_slug"
    template_name = "steps/step_form.html"
    success_url = 'step_detail'

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StepUpdateView, self).get_context_data(**kwargs)

        if self.object:
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object

        for key in ['step_slug', 'action_slug']:
            if key in self.kwargs:
                ctx_key = key.split('_')[0]
                context[ctx_key] = self.object.nodes[self.kwargs[key]]
        
        context['form'] = self.form_class(initial=context['step'])

        if 'form' in kwargs:
            print "FORM IN KWARGS"
            context['form'] = kwargs['form']

        #if not 'form' in kwargs:
        #context['form'] = self.form_class(initial=context['step'])
        #else:
        #    context['form'] = kwargs['form']

        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        self.object = self.get_object()
        #context = self.get_context_data(**kwargs)
        #args = self.get_form_kwargs()
        form = self.form_class(request.POST)

        if form.is_valid():
            print "FORM VALID"
            return self.form_valid(form)
        else:
            print "FORM INVALID"
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        step = context['step']

        data = form.cleaned_data.items()
        step.update(data)   # THIS KEEPS IT FROM DESTROYING THE ACTIONS ATTACHED TO THE STEP

        self.object.save()

        messages.add_message(self.request, messages.INFO, "Your step was updated.")
        return HttpResponseRedirect(self.get_success_url())

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

    def get_url_args(self):
        protocol = self.get_protocol()
        context = self.get_context_data()
        return {'owner_slug':protocol.owner.slug, 'protocol_slug': protocol.slug, 'step_slug':context['step'].slug}


class ActionDetailView(AuthorizedForProtocolMixin, DetailView):

    model = Protocol
    template_name = "actions/action_detail.html"
    slug_url_kwarg = "protocol_slug"

    def get_context_data(self, **kwargs):
        context = super(ActionDetailView, self).get_context_data(**kwargs)
        action_slug = self.kwargs['action_slug']
        context['action'] = self.object.nodes[action_slug]
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
        context['step'] = self.object.nodes[step_slug]
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
        data = dict(form.cleaned_data.items() + verb_form.cleaned_data.items())
        #ADD THE VERB
        verb_slug = self.kwargs.get('verb_slug', None)
        data['verb'] = verb_slug

        action = Action(protocol, step=step, data=data)

        if 'actions' in step:
            step['actions'].append(action)
        else:
            step['actions'] = [action]
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your action was added.")
        return super(ActionCreateView, self).form_valid(form)

    #def get_context_data(self, **kwargs):
    #    context = super(ActionCreateView, self).get_context_data(**kwargs)
    #    step_slug = self.kwargs['step_slug']
    #    context['step'] = self.object.nodes[step_slug]
    #    context['form'] = ActionForm()
    #    return context

class ActionUpdateView(LoginRequiredMixin, AuthorizedForProtocolMixin, AuthorizedforProtocolEditMixin, UpdateView):

    model = Protocol
    form_class = ActionForm
    slug_url_kwarg = "protocol_slug"
    template_name = "actions/action_form.html"
    success_url = 'action_detail'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ActionUpdateView, self).get_context_data(**kwargs)

        if self.object:
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object

        for key in ['step_slug', 'action_slug']:
            if key in self.kwargs:
                ctx_key = key.split('_')[0]
                context[ctx_key] = self.object.nodes[self.kwargs[key]]
        
        context['verb_form'] = VERB_FORM_DICT[context['action']['verb']](initial=context['action'], prefix='verb')
        context['verb_name'] = context['verb_form'].name
        context['form'] = self.form_class(initial=context['action'], prefix='action')

        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        args = self.get_form_kwargs()

        form = self.form_class(request.POST, prefix='action')

        verb_key = context['action']['verb']
        print context['action']
        print verb_key
        verb_form = VERB_FORM_DICT[verb_key](request.POST, prefix='verb')

        if form.is_valid() and verb_form.is_valid():
            print "FORM VALID"
            return self.form_valid(form, verb_form)
        else:
            print "FORM INVALID"
            return self.form_invalid(form, verb_form)

    def form_valid(self, form, verb_form):
        '''Takes in two forms for processing'''
        protocol = self.get_protocol()
        context = self.get_context_data()
        step = context['step']
        action = context['action']

        # COMBINE THE DATA FROM THE TWO FORMS
        data = dict(form.cleaned_data.items() + verb_form.cleaned_data.items())
        #ADD THE VERB
        #verb_slug = self.kwargs.get('verb_slug', None)
        data['verb'] = action['verb']

        # UPDATE THE ACTION VALUES WITH THE CLEANED DATA
        action.update(data)

        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your action was updated.")
        return HttpResponseRedirect(self.get_success_url())


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

    def get_url_args(self):
        protocol = self.get_protocol()
        context = self.get_context_data()
        return {'protocol_slug': protocol.slug, 'step_slug':context['step'].slug, 'action_slug': context['action'].slug}


class NodeDeleteView(DeleteView):
    model = Protocol
    slug_url_kwarg = "protocol_slug"

    def post(self):
        print "I DID A POST"

    def get(self):
        print "I DID A GET"

