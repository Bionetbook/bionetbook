# Create your views here.
from django import forms, http
from django.http import Http404, HttpResponse
from django.views.generic import ListView, View, CreateView, FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView
from django.utils import simplejson

from django.template.defaultfilters import slugify
from braces.views import LoginRequiredMixin
from schedule.forms import CalendarForm, CalendarManualForm
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
    template_name = "schedule/single_calendar.html"
    slug_url_kwarg = "calendar_slug"
    def get_context_data(self, **kwargs):
        context = super(ScheduleAPI,self).get_context_data(**kwargs)

        calendars = self.request.user.calendar_set.get(pk=self.kwargs['pk'])
        if calendars:
            context['calendar'] = calendars
        else:
            context['calendar'] = None

        organizations = self.request.user.organization_set.all()

        if organizations:
            context['organization'] = organizations[0]
        else:
            context['organization'] = None

        experiements = self.request.user.experiment_set.all()
        if experiements:
            context['experiment'] = experiements[0]
        else:
            context['experiment'] = None

        return context


class CalendarListView(LoginRequiredMixin, ListView):
    model = Calendar
    template_name = "schedule/calendar_list.html"
    slug_url_kwarg = "owner_slug"
    def get_context_data(self, **kwargs):
        context = super(CalendarListView, self).get_context_data(**kwargs)
        calendarList = self.request.user.calendar_set.all()
        if calendarList:
            context['calendars'] = calendarList
        else:
            context['calendars'] = None

        return context

    # def get(self, request, *args, **kwargs):  
    #   # context = Calendar.objects.all()[1].expToCalendar()
    #   # return HttpResponse(simplejson.dumps(context),mimetype='application/json')
    #   context = self.get_context_data()
    #   context['calendar'] = Calendar.objects.all()[0]
    #   return self.render_to_response(context)

class ScheduleExample(TemplateView):
    template_name = "schedule/schedule_example.html"


class CalendarCreateView(LoginRequiredMixin, FormView):
    model = Calendar
    form_class = CalendarManualForm
    template_name = "schedule/calendar_form.html"

    def form_valid(self, form):
        cal = Calendar()
        cal.user = self.request.user
        cal.name = form.cleaned_data['name']
        cal.data = None
        cal.slug = slugify(cal.name)
        cal.save()
        return HttpResponseRedirect(cal.get_absolute_url())

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form(self, form_class):
        form = form_class(**self.get_form_kwargs())
        return form

