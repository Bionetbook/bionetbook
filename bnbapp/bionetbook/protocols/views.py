from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django import forms, http
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView, PathMixin

from protocols.forms import ProtocolPublishForm, StepForm, ActionForm, ComponentForm, MachineForm, ThermocyclerForm, OrganizationListForm
from protocols.forms.baseforms import ProtocolForm
from protocols.models import Protocol, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
from compare.models import ProtocolPlot
from protocols.utils import VERB_CHOICES, VERB_FORM_DICT


#####################
# MIXINS
#####################




#####################
# BASE CLASSES
#####################

class NodeDetailView(LoginRequiredMixin, AuthorizedOrganizationMixin, DetailView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    slugs = []

    def get_context_data(self, **kwargs):

        context = super(NodeDetailView, self).get_context_data(**kwargs)

        for slug in self.slugs:
            objectid = self.kwargs[slug]
            if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF
                slug = slug[:-5]
            context[slug] = self.object.nodes[objectid]

        return context


class NodeCreateViewBase(LoginRequiredMixin, AuthorizedOrganizationMixin, SingleObjectMixin, FormView):
    '''This view needs to properly create a view, set a form and process the form'''

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    form_class = StepForm
    success_url = None
    form_prefix = None
    slugs = []

    # def get_url_args(self):
    #     protocol = self.get_protocol()
    #     result = {'owner_slug':protocol.owner.slug, 'protocol_slug': protocol.slug}

    #     if self.slugs:
    #         context = self.get_context_data()
    #         for slug in self.slugs:
    #             label = self.kwargs[slug]
    #             if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF FOR THE context OBJECT
    #                 slug = slug[:-5]
    #             result[slug] = context[label].slug

    #     return result

    def get_url_args(self):
        args = {'protocol_slug': self.object.slug, 'owner_slug':self.object.owner.slug}

        if self.slugs:
            context = self.get_context_data()
            for slug in self.slugs:
                objectid = slug
                if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF
                    objectid = slug[:-5]

                args[slug] = context[objectid].slug

        return args


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
        context = super(NodeCreateViewBase, self).get_context_data(**kwargs)

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

        for slug in self.slugs:
            label = self.kwargs[slug]
            if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF
                slug = slug[:-5]
            context[slug] = self.object.nodes[label]

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
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class NodeUpdateView(LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, UpdateView):

    slugs = []
    node_type = None

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

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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
        context = super(NodeUpdateView, self).get_context_data(**kwargs)

        if self.object:
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        
        for slug in self.slugs:
            label = self.kwargs[slug]
            if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF FOR THE context OBJECT
                slug = slug[:-5]
            context[slug] = self.object.nodes[label]

        if 'form' in kwargs:
            context['form'] = kwargs['form']
        else:
            context['form'] = self.form_class( initial=context[self.node_type] )

        return context

    def get_url_args(self):
        args = {'protocol_slug': self.object.slug, 'owner_slug':self.object.owner.slug}
        context = self.get_context_data()

        if self.slugs:
            context = self.get_context_data()
            for slug in self.slugs:
                objectid = slug
                if slug[-5:] == '_slug':        # STRIP THE _slug SUFFIX OFF
                    objectid = slug[:-5]

                args[slug] = context[objectid].slug

        return args

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        self.object = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        node = context[self.node_type]

        data = form.cleaned_data.items()
        node.update(data)   # THIS KEEPS IT FROM DESTROYING THE ACTIONS ATTACHED TO THE STEP

        self.object.save()

        messages.add_message(self.request, messages.INFO, "Your %s, \"%s\", was updated." % ( self.node_type, node.title ))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class NodeDeleteView(LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    template_name = "protocols/node_delete.html"
    slugs = []
    node_type = None
    cancel_parent_redirect = False

    def cancel(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = None

        if self.node_type:
            slug = self.kwargs['%s_slug' % self.node_type]

        if slug and slug in self.object.nodes:
            if self.cancel_parent_redirect:         # REDIRECT TO THE PARENT'S DETAIL PAGE ON CANCEL
                url = self.object.nodes[slug].parent.get_absolute_url()
            else:
                url = self.object.nodes[slug].get_absolute_url()
        else:
            url = self.object.get_absolute_url()

        return http.HttpResponseRedirect(url)


    # def confirm(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     #print "NODE DELETED"

    #     messages.add_message(self.request, messages.INFO, "Your node was deleted.")
    #     url = self.object.get_absolute_url()
    #     return http.HttpResponseRedirect(url)


    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()                     # <- NEEDED?
        slug = self.kwargs['%s_slug' % self.node_type]
        obj = self.object.nodes[slug]
        parent = obj.parent
        message = "The %s \"%s\" was deleted." % (self.node_type, obj['name'])
        self.object.delete_node(obj['objectid'])
        self.object.save()
        messages.add_message(self.request, messages.INFO, message)
        url = parent.get_absolute_url()
        return http.HttpResponseRedirect(url)

    # def get_context_data(self, **kwargs):
    #     context = super(NodeDeleteView, self).get_context_data(**kwargs)
    #     slug = self.kwargs['%s_slug' % self.node_type]
    #     context[self.node_type] = self.object.nodes[slug]
    #     return context


#####################
# PROTOCOLS
#####################

# class ProtocolDetailView(LoginRequiredMixin, AuthorizedOrganizationMixin, DetailView):

#     model = Protocol
#     slug_url_kwarg = "protocol_slug"

#     def get_context_data(self, **kwargs):
#         context = super(ProtocolDetailView, self).get_context_data(**kwargs)
#         context['steps'] = self.object.steps
#         return context

# class PathMixin(object):
#     def get_context_data(self, **kwargs):
#         context = super(PathMixin, self).get_context_data(**kwargs)
#         context['paths'] = [{'name':"Dashboard", 'icon':'home', 'url':reverse('dashboard')}]
#         return context 


class ProtocolSetupMixin(PathMixin):
    def get_context_data(self, **kwargs):
        context = super(ProtocolSetupMixin, self).get_context_data(**kwargs)

        owner_slug = self.kwargs.get('owner_slug', None)
        if owner_slug:
            context['organization'] = Organization.objects.get(slug=owner_slug)
            context['paths'].append( { 'name':context['organization'].name, 'url':context['organization'].get_absolute_url() } )

        protocol_slug = self.kwargs.get('protocol_slug', None)
        if protocol_slug:
            context['protocol'] = Protocol.objects.get(slug=protocol_slug)
            context['paths'].append( { 'name':context['protocol'].name, 'url':context['protocol'].get_absolute_url() } )

        return context 


# class ProtocolPathMixin(PathMixin):
#     def get_context_data(self, **kwargs):
#         context = super(ProtocolPathMixin, self).get_context_data(**kwargs)
#         # context['paths'].append( {'name':"Dashboard", 'icon':'home', 'url':reverse('dashboard')} )
#         return context 


class ProtocolDetailView(ProtocolSetupMixin, LoginRequiredMixin, AuthorizedOrganizationMixin, TemplateView):
    template_name = "protocols/protocol_layout_single.html"           

    def get_context_data(self, **kwargs):
        context = super(ProtocolDetailView, self).get_context_data(**kwargs)
        del(context['paths'][-1]['url'])
        return context


class ProtocolListView(LoginRequiredMixin, ListView):

    model = Organization
    template_name = "protocols/protocol_list.html"
    slug_url_kwarg = "owner_slug"

    # def get_context_data(self, **kwargs):
    #     context = super(ProtocolCreateView, self).get_context_data(**kwargs)
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     if slug:
    #         context['organization'] = Organization.objects.get(slug=slug)
    #     return context

    def get_queryset(self):
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if slug:
            self.object = Organization.objects.get(slug=slug)
            return Organization.objects.filter(slug=slug)
        else:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return Organization.objects.all()    # GET ALL THE PROTOCOLS
            if self.request.user.is_authenticated():
                #return self.request.user.organizations.protocols
                # return Protocol.objects.filter(
                #         Q(status=Protocol.STATUS_PUBLISHED) |
                #         Q(owner=self.request.user)
                #         )
                return self.request.user.organization_set.all() # GET ALL THE ORGANIZATIONS THE USER IS A MEMEBER OF
            return []

    def get_context_data(self, **kwargs):
        context = super(ProtocolListView, self).get_context_data(**kwargs)
        context['organization'] = self.object
        return context


class ProtocolCreateView(ProtocolSetupMixin, LoginRequiredMixin, CreateView):
    '''
    View used to create new protocols
    '''

    model = Protocol
    form_class = ProtocolForm
    slug_url_kwarg = "owner_slug"

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super(ProtocolCreateView, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(ProtocolCreateView, self).get_context_data(**kwargs)
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     if slug:
    #         context['organization'] = Organization.objects.get(slug=slug)
    #     return context

    def get_context_data(self, **kwargs):
        context = super(ProtocolCreateView, self).get_context_data(**kwargs)
        context['paths'].append( { 'name':'New Protocol' } )
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        org = Organization.objects.get(slug=slug)

        form.instance.owner = org
        form.instance.author = self.request.user

        return super(ProtocolCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = form_class(**self.get_form_kwargs())
        # form.fields['owner'].choices = [(org.pk, org.name) for org in self.request.user.organization_set.all()]
        # NEED TO CHANGE THE FORM CLASS'S QUERYSET ON THE FIELD
        return form


class ProtocolUpdateView(ProtocolSetupMixin, LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, UpdateView):

    model = Protocol
    form_class = ProtocolForm
    slug_url_kwarg = "protocol_slug"

    # NEED TO ONLY RETURN A PROTOCOL WHO'S PUBLISH IS SET TO False

    #slug_url_kwarg = "owner_slug"

    # def get_context_data(self, **kwargs):
    #     context = super(ProtocolCreateView, self).get_context_data(**kwargs)
    #     # slug = self.kwargs.get("owner_slug", None)
    #     # if slug:
    #     #     context['organization'] = Organization.objects.get(slug=slug)
    #     print "FOO"
    #     print self.object
    #     context['organization'] = self.object.owner
    #     return context

    def get_context_data(self, **kwargs):
        context = super(ProtocolUpdateView, self).get_context_data(**kwargs)
        context['steps'] = self.object.steps
        context['organization'] = self.object.owner
        context['paths'].append( { 'name':'Edit' } )
        return context

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


class ProtocolPublishView(LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    template_name = "protocols/protocol_publish_form.html"

    def cancel(self, request, *args, **kwargs):
        self.object = self.get_object()
        url = self.object.get_absolute_url()
        return http.HttpResponseRedirect(url)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.published = True
        self.object.save()
        messages.add_message(self.request, messages.INFO, "Your protocol is published.")
        url = self.object.get_absolute_url()
        return http.HttpResponseRedirect(url)

class ProtocolPublicView(LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView):

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    template_name = "protocols/protocol_public_form.html"

    def cancel(self, request, *args, **kwargs):
        self.object = self.get_object()
        url = self.object.get_absolute_url()
        return http.HttpResponseRedirect(url)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.public = True
        self.object.save()
        messages.add_message(self.request, messages.INFO, "Your protocol is now public.")
        url = self.object.protocol_outline_url()
        return http.HttpResponseRedirect(url)


class ProtocolDuplicateView(LoginRequiredMixin, AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView):

    # NEED TO VALIDATE THE FORM TO GET THE OWNER
    # NEED TO CONFIRM THE PROTOCOL IS PUBLISHED BEFORE DUPLICATING

    model = Protocol
    slug_url_kwarg = "protocol_slug"
    template_name = "protocols/protocol_duplicate_form.html"
    form_class = OrganizationListForm

    def get_context_data(self, **kwargs):
        context = super(ProtocolDuplicateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['form'].fields['owner'].choices = [(org.pk, org.name) for org in self.request.user.organization_set.all()] 
        return context

    def cancel(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.add_message(self.request, messages.INFO, "Your protocol duplication was canceled.")
        url = self.object.get_absolute_url()
        return http.HttpResponseRedirect(url)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.form_class(request.POST)
        new_owner = request.user.organization_set.get(pk=request.POST['owner'])

        #print new_owner
        self.object.clone(owner=new_owner)
        self.object.save()
        messages.add_message(self.request, messages.INFO, "Your protocol has been duplicated.")
        url = self.object.get_absolute_url()
        return http.HttpResponseRedirect(url)


#####################
# STEPS
#####################


class StepDetailView(NodeDetailView):

    model = Protocol
    template_name = "steps/step_detail.html"
    slug_url_kwarg = "protocol_slug"
    slugs = ['step_slug']


class StepCreateView(NodeCreateViewBase):
    '''Creates and appends a step to a protocol.'''

    template_name = "steps/step_create.html"
    form_class = StepForm
    success_url = 'protocol_detail'

    def form_valid(self, form):
        protocol = self.get_protocol()
        new_step = Step(protocol, data=form.cleaned_data)
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your step \'%s\'' was added." % new_step.title)
        return super(StepCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class StepUpdateView(NodeUpdateView):
    model = Protocol
    form_class = StepForm
    slug_url_kwarg = "protocol_slug"
    template_name = "steps/step_form.html"
    success_url = 'step_detail'
    slugs = ['step_slug']
    node_type = "step"


class StepDeleteView(NodeDeleteView):
    template_name = "steps/step_delete.html"
    node_type = "step"

    def get_context_data(self, **kwargs):
        context = super(StepDeleteView, self).get_context_data(**kwargs)
        step_slug = self.kwargs['step_slug']
        context['step'] = self.object.nodes[step_slug]
        return context

    # def cancel(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     step_slug = self.kwargs['step_slug']
        
    #     if step_slug in self.object.nodes:
    #         url = self.object.nodes[step_slug].get_absolute_url()
    #     else:
    #         url = self.object.get_absolute_url()

    #     return http.HttpResponseRedirect(url)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        step_slug = self.kwargs['step_slug']
        step = self.object.nodes[step_slug]
        parent = step.parent
        message = "The Step \"%s\" was deleted." % step['name']
        self.object.delete_node(step['objectid'])
        self.object.save()
        messages.add_message(self.request, messages.INFO, message)
        url = parent.get_absolute_url()
        return http.HttpResponseRedirect(url)


#####################
# ACTIONS
#####################


class ActionDetailView(NodeDetailView):

    #model = Protocol
    template_name = "actions/action_detail.html"
    slugs = ['step_slug', 'action_slug']


class ActionVerbListView(AuthorizedOrganizationMixin, DetailView):

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


class ActionCreateView(NodeCreateViewBase):

    form_class = ActionForm # THIS WILL ONLY COVER ONE OF TWO FORMS
    template_name = "actions/action_create.html"
    success_url = 'step_detail'
    form_prefix = 'action'
    slugs = ['step_slug']

    def get_context_data(self, **kwargs):
        '''Ads the Verb form to the context'''
        context = super(ActionCreateView, self).get_context_data(**kwargs)

        verb_slug = context['verb_slug']
        if not 'verb_form' in kwargs:
            context['verb_form'] = VERB_FORM_DICT[verb_slug](prefix='verb')
            context['verb_name'] = context['verb_form'].name

        if 'protocol_id' in context['verb_form'].fields:        # POPULATE THE protocol_id CHOICES WITH OPTIONS THE USER HAS ACCESS TO
            context['verb_form'].fields['protocol_id'].choices = self.request.user.profile.get_all_published_protocol_choices()

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

        data = dict(form.cleaned_data.items() + verb_form.cleaned_data.items())     # COMBINE THE DATA FROM THE TWO FORMS
        verb_slug = self.kwargs.get('verb_slug', None)                              # ADD THE VERB
        data['verb'] = verb_slug

        action = Action(protocol, parent=step, data=data)

        if 'actions' in step:
            step['actions'].append(action)
        else:
            step['actions'] = [action]
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your action was added.")
        return super(ActionCreateView, self).form_valid(form)


class ActionUpdateView(NodeUpdateView):

    model = Protocol
    form_class = ActionForm
    slug_url_kwarg = "protocol_slug"
    template_name = "actions/action_form.html"
    success_url = 'action_detail'
    slugs = ['step_slug', 'action_slug']
    node_type = "action"

    def get_context_data(self, form=None, verb_form=None, **kwargs):
        context = super(ActionUpdateView, self).get_context_data(**kwargs)

        if form:
            context['verb_form'] = verb_form
        else:
            context['verb_form'] = VERB_FORM_DICT[context[self.node_type]['verb']](initial=context[self.node_type], prefix='verb')
        context['verb_name'] = context['verb_form'].name

        if 'protocol_id' in context['verb_form'].fields:        # POPULATE THE protocol_id CHOICES WITH OPTIONS THE USER HAS ACCESS TO
            context['verb_form'].fields['protocol_id'].choices = self.request.user.profile.get_all_published_protocol_choices()

        if form:
            context['form'] = form
        else:
            context['form'] = self.form_class(initial=context[self.node_type], prefix=self.node_type)
        
        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        args = self.get_form_kwargs()
        form = self.form_class(request.POST, prefix=self.node_type)
        verb_key = context[self.node_type]['verb']
        verb_form = VERB_FORM_DICT[verb_key](request.POST, prefix='verb')

        if form.is_valid() and verb_form.is_valid():
            return self.form_valid(form, verb_form)
        else:
            return self.form_invalid(form, verb_form)

    def form_valid(self, form, verb_form):
        '''Takes in two forms for processing'''
        protocol = self.get_protocol()
        context = self.get_context_data()
        node = context[self.node_type]

        # COMBINE THE DATA FROM THE TWO FORMS
        data = dict(form.cleaned_data.items() + verb_form.cleaned_data.items())
        data['verb'] = node['verb']

        # UPDATE THE ACTION VALUES WITH THE CLEANED DATA
        node.update(data)
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your %s, \"%s\", was updated." % ( self.node_type, node.title ))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, verb_form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        ctx = self.get_context_data(object=self.object, form=form, verb_form=verb_form)
        return self.render_to_response(ctx)


class ActionDeleteView(NodeDeleteView):
    template_name = "actions/action_delete.html"
    node_type = "action"

    def get_context_data(self, **kwargs):
        context = super(ActionDeleteView, self).get_context_data(**kwargs)
        slug = self.kwargs['action_slug']
        context['action'] = self.object.nodes[slug]
        context['step'] = context['action'].parent       #NOT SURE IF THIS IS BETTER THEN THE ABOVE TECHNIQUE
        return context

    # def cancel(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     slug = self.kwargs['action_slug']

    #     if slug in self.object.nodes:
    #         url = self.object.nodes[slug].get_absolute_url()
    #     else:
    #         url = self.object.get_absolute_url()

    #     return http.HttpResponseRedirect(url)

    # def confirm(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     slug = self.kwargs['action_slug']
    #     action = self.object.nodes[slug]
    #     parent = action.parent
    #     message = "The Action \"%s\" was deleted." % action['name']
    #     self.object.delete_node(action['objectid'])
    #     self.object.save()
    #     messages.add_message(self.request, messages.INFO, message)
    #     url = parent.get_absolute_url()
    #     return http.HttpResponseRedirect(url)


    # def confirm(self, request, *args, **kwargs):
    #     self.object = self.get_object()                     # <- NEEDED?
    #     slug = self.kwargs['%s_slug' % self.node_type]
    #     obj = self.object.nodes[slug]
    #     parent = obj.parent
    #     message = "The %s \"%s\" was deleted." % (self.node_type, self['name'])
    #     self.object.delete_node(obj['objectid'])
    #     # self.object.save()
    #     messages.add_message(self.request, messages.INFO, message)
    #     url = parent.get_absolute_url()
    #     return http.HttpResponseRedirect(url)



#####################
# COMPONENTS
#####################



    # def form_valid(self, form):

    #     if form.has_changed():

    #     super(NodeCreateViewBase, self).form_valid(form)


class ComponentDetailView(NodeDetailView):
    template_name = "component/component_detail.html"
    slugs = ['step_slug', 'action_slug', 'component_slug']


class ComponentCreateView(NodeCreateViewBase):
    '''Creates and appends a component to an action.'''

    form_class = ComponentForm
    template_name = "component/component_form.html"
    success_url = "action_detail"
    slugs = ['step_slug', 'action_slug']

    def form_valid(self, form):
        protocol = self.get_protocol()
        context = self.get_context_data()
        new_item = Component(protocol, parent=context['action'], data=form.cleaned_data)
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your component \'%s\'' was added." % new_item.title)
        return super(ComponentCreateView, self).form_valid(form)


class ComponentUpdateView(NodeUpdateView):
    model = Protocol
    form_class = ComponentForm
    slug_url_kwarg = "protocol_slug"
    template_name = "component/component_form.html"
    success_url = "action_detail"
    node_type = "component"
    slugs = ['step_slug', 'action_slug', 'component_slug']

    # def get_context_data(self, form = None, **kwargs):
    #     context = super(MachineUpdateView, self).get_context_data(**kwargs)
    #     context['component'] = self.object.nodes[componenet_slug]
    #     context['form'] = self.form_class(initial = context['component'])
    #     return context

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:                                    # COULD DEFAULT TO THE PARENT URL
            args = self.get_url_args()
            args.pop('component_slug')
            url = reverse(self.success_url, kwargs=args)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

class ComponentDeleteView(NodeDeleteView):
    template_name = "component/component_delete.html"
    node_type = "component"
    cancel_parent_redirect = True

    def get_context_data(self, **kwargs):
        context = super(ComponentDeleteView, self).get_context_data(**kwargs)
        slug = self.kwargs['%s_slug' % self.node_type]
        context[self.node_type] = self.object.nodes[slug]
        context['action'] = context[self.node_type].parent       #NOT SURE IF THIS IS BETTER THEN THE ABOVE TECHNIQUE
        return context

    # def cancel(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     slug = self.kwargs['%s_slug' % self.node_type]

    #     if slug in self.object.nodes:
    #         url = self.object.nodes[slug].get_absolute_url()
    #     else:
    #         url = self.object.get_absolute_url()

    #     return http.HttpResponseRedirect(url)

    # def confirm(self, request, *args, **kwargs):
    #     self.object = self.get_object()                     # <- NEEDED?
    #     slug = self.kwargs['%s_slug' % self.node_type]
    #     obj = self.object.nodes[slug]
    #     parent = obj.parent
    #     message = "The %s \"%s\" was deleted." % (self.node_type, self['name'])
    #     self.object.delete_node(obj['objectid'])
    #     # self.object.save()
    #     messages.add_message(self.request, messages.INFO, message)
    #     url = parent.get_absolute_url()
    #     return http.HttpResponseRedirect(url)


#####################
# MACHINES
#####################

class MachineDetailView(NodeDetailView):
    slugs = ['step_slug', 'action_slug', 'machine_slug']
    template_name = "machine/machine_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MachineDetailView, self).get_context_data(**kwargs)
        context['machine'] = context['action']['machine']
        return context

class MachineCreateView(NodeCreateViewBase):
    '''Creates and appends a thermocycle to an action.'''

    form_class = MachineForm
    template_name = "machine/machine_form.html"
    success_url = "action_detail"
    slugs = ['step_slug', 'action_slug']

    def form_valid(self, form):
        protocol = self.get_protocol()
        context = self.get_context_data()
        new_item = Machine(protocol, parent=context['action'], data=form.cleaned_data)
        protocol.save()
        print "PROTOCOL SAVED"

        messages.add_message(self.request, messages.INFO, "Your machine \'%s\'' was added." % new_item.title)
        return super(MachineCreateView, self).form_valid(form)          # DOES NOT SEEM RIGHT

class MachineUpdateView(NodeUpdateView):
    model = Protocol
    form_class = MachineForm
    slug_url_kwarg = "protocol_slug"
    template_name = "machine/machine_form.html"
    success_url = "machine_detail"
    node_type = "machine"
    slugs = ['step_slug', 'action_slug', 'machine_slug']

    def get_context_data(self, form = None, **kwargs):
        context = super(MachineUpdateView, self).get_context_data(**kwargs)
        context['machine'] = context['action']['machine']
        context['form'] = self.form_class(initial = context['machine'])
        return context


class MachineDeleteView(NodeDeleteView):
    template_name = "machine/machine_delete.html"
    node_type = "machine"
    cancel_parent_redirect = True

    def get_context_data(self, **kwargs):
        context = super(MachineDeleteView, self).get_context_data(**kwargs)
        slug = self.kwargs['%s_slug' % self.node_type]
        context[self.node_type] = self.object.nodes[slug]
        context['action'] = context[self.node_type].parent       #NOT SURE IF THIS IS BETTER THEN THE ABOVE TECHNIQUE
        return context

#####################
# THEMOCYCLERS
#####################


class ThermocycleDetailView(NodeDetailView):
    template_name = "thermocycle/thermocycle_detail.html"
    slugs = ['step_slug', 'action_slug', 'thermocycle_slug']


class ThermocycleCreateView(NodeCreateViewBase):
    '''Creates and appends a thermocycle to an action.'''

    form_class = ThermocyclerForm
    template_name = "thermocycle/thermocycle_form.html"
    success_url = "action_detail"
    slugs = ['step_slug', 'action_slug']

    def form_valid(self, form):
        protocol = self.get_protocol()
        context = self.get_context_data()
        new_item = Thermocycle(protocol, parent=context['action'], data=form.cleaned_data)
        protocol.save()

        messages.add_message(self.request, messages.INFO, "Your thermocycle \'%s\'' was added." % new_item.title)
        return super(ThermocycleCreateView, self).form_valid(form)


class ThermocycleUpdateView(NodeUpdateView):
    model = Protocol
    form_class = ThermocyclerForm
    slug_url_kwarg = "protocol_slug"
    template_name = "thermocycle/thermocycle_form.html"
    success_url = "action_detail"
    slugs = ['step_slug', 'action_slug', 'thermocycle_slug']
    node_type = "thermocycle"

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            args = self.get_url_args()
            args.pop('thermocycle_slug')
            url = reverse(self.success_url, kwargs=args)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url


class ThermocycleDeleteView(NodeDeleteView):
    template_name = "thermocycle/thermocycle_delete.html"
    node_type = "thermocycle"
    cancel_parent_redirect = True

    def get_context_data(self, **kwargs):
        context = super(ThermocycleDeleteView, self).get_context_data(**kwargs)
        slug = self.kwargs['%s_slug' % self.node_type]
        context[self.node_type] = self.object.nodes[slug]
        context['action'] = context[self.node_type].parent       #NOT SURE IF THIS IS BETTER THEN THE ABOVE TECHNIQUE
        return context

    # def cancel(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     slug = self.kwargs['%s_slug' % self.node_type]

    #     if slug in self.object.nodes:
    #         url = self.object.nodes[slug].get_absolute_url()
    #     else:
    #         url = self.object.get_absolute_url()

    #     return http.HttpResponseRedirect(url)

    # def confirm(self, request, *args, **kwargs):
    #     self.object = self.get_object()                     # <- NEEDED?
    #     slug = self.kwargs['%s_slug' % self.node_type]
    #     obj = self.object.nodes[slug]
    #     parent = obj.parent
    #     message = "The %s \"%s\" was deleted." % (self.node_type, self['name'])
    #     self.object.delete_node(obj['objectid'])
    #     # self.object.save()
    #     messages.add_message(self.request, messages.INFO, message)
    #     url = parent.get_absolute_url()
    #     return http.HttpResponseRedirect(url)
