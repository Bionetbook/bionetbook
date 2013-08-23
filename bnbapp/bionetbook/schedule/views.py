# Create your views here.
from django import forms, http
from django.http import Http404, HttpResponse
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView
from django.utils import simplejson

from braces.views import LoginRequiredMixin

from protocols.models import Protocol, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
from schedule.models import Calendar
from experiment.models import Experiment
from protocols.utils import VERB_CHOICES, VERB_FORM_DICT

# class ScheduleListView(LoginRequiredMixin, ListView):
#   model = Organization
#   template_name = "schedule/schedule_list.html"
#   slug_url_kwarg = "owner_slug"

#   def get_queryset(self):
#       slug = self.kwargs.get(self.slug_url_kwarg, None)

#       if slug:
#           self.object = Organization.objects.get(slug=slug)
#           return Organization.objects.filter(slug=slug)
#       else:
#           if self.request.user.is_superuser or self.request.user.is_staff:
#               return Organization.objects.all()
#           if self.request.user.is_authenticated():
#               return self.request.user.organization_set.all()
#           return []


#   def get_context_data(self, **kwargs):
#       context = super(ScheduleListView, self).get_context_data(**kwargs)
#       context['organization'] = self.object
#       return context

class ScheduleAPI(LoginRequiredMixin, TemplateView):
    template_name = "schedule/schedule_list.html"
    slug_url_kwarg = "owner_slug"
    def get_context_data(self, **kwargs):
        context = super(ScheduleAPI,self).get_context_data(**kwargs)

        organizations = self.request.user.organization_set.all()
        if organizations:
            context['organization'] = organizations[0]
        else:
            context['organization'] = None

        calendars = self.request.user.calendar_set.all()
        if calendars:
            context['calendar'] = calendars[0]
        else:
            context['calendar'] = None

        experiements = self.request.user.experiment_set.all()
        if experiements:
            context['experiment'] = experiements[0]
        else:
            context['experiment'] = None

        return context

    # def get(self, request, *args, **kwargs):
    #   # context = Calendar.objects.all()[1].expToCalendar()
    #   # return HttpResponse(simplejson.dumps(context),mimetype='application/json')
    #   context = self.get_context_data()
    #   context['calendar'] = Calendar.objects.all()[0]
    #   return self.render_to_response(context)

