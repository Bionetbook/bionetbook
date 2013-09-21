from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from django.utils.log import getLogger
from django.views.generic.detail import SingleObjectMixin
from django import http
from django.core.urlresolvers import reverse
# import django.template as template

from braces.views import LoginRequiredMixin

from core.utils import check_owner_edit_authorization, check_owner_view_authorization
from protocols.models import Protocol

logger = getLogger('django.request')


# class PathGenerator(template.Node):
#     def render(self, context):
#         return "FOO"


#####################
# MIXINS
#####################

class PathMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PathMixin, self).get_context_data(**kwargs)
        context['paths'] = [{'name':"Dashboard", 'icon':'home', 'url':reverse('dashboard')}]
        return context 


#####################
# VIEWS
#####################

class DashboardView(PathMixin, LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        del(context['paths'][-1]['url'])

        context['titleBlock'] = {'prefix':str(self.request.user) + "\'s", 'title':'Dashboard', 'suffix':""}
        
        return context


class DocumentationView(TemplateView):
    template_name = "core/documentation.html"


class FAQView(TemplateView):
    template_name = "core/FAQ.html"    


class ReleaseNotes(TemplateView):
    template_name = "core/release_notes.html"        


class ConfirmationMixin(object):
    '''
    Simple view that handles a basic confirmation dialogue.  It expects a 
    form to have two buttons named "confirm" and "cancel".  If there is a 
    POST request made, either of these two objects will be called.  The 
    GET request simply presents the dialogue as a form.
    '''

    permanent = False
    cancel_url = None
    confirm_button_name = "confirm"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if self.confirm_button_name in request.POST:
            return self.confirm(request, *args, **kwargs)
        return self.cancel(request, *args, **kwargs)

    def confirm(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def cancel(self, request, *args, **kwargs):
        url = self.get_cancel_url(request, *args, **kwargs)
        if url:
            if self.permanent:
                return http.HttpResponsePermanentRedirect(url)
            else:
                return http.HttpResponseRedirect(url)
        else:
            logger.warning('Gone: %s', self.request.path,
                        extra={
                            'status_code': 410,
                            'request': self.request
                        })
            return http.HttpResponseGone()


    def get_cancel_url(self, request, *args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the
        URL pattern match generating the redirect request
        are provided as kwargs to this method.
        """
        if self.cancel_url:
            url = self.cancel_url % kwargs
            args = self.request.META.get('QUERY_STRING', '')
            if args and self.query_string:
                url = "%s?%s" % (url, args)
            return url
        else:
            return None


class ConfirmationObjectView(ConfirmationMixin, SingleObjectMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def confirm(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
