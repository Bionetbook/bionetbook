# Create your views here.
from django import forms, http
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from core.views import AuthorizedOrganizationMixin, AuthorizedOrganizationEditMixin, ConfirmationObjectView

from protocols.models import Protocol, Step, Action, Thermocycle, Machine, Component
from organization.models import Organization
<<<<<<< HEAD
from schedule.models import Calendar
=======

from schedule.models import Calendar
from schedule.models import Schedule, Event

>>>>>>> 354ff353735d887129640d79764e481667e132a9

from protocols.utils import VERB_CHOICES, VERB_FORM_DICT

class ScheduleListView(LoginRequiredMixin, ListView):
	model = Organization
	template_name = "schedule/schedule_list.html"
	slug_url_kwarg = "owner_slug"

	def get_queryset(self):
		slug = self.kwargs.get(self.slug_url_kwarg, None)

		if slug:
			self.object = Organization.objects.get(slug=slug)
			return Organization.objects.filter(slug=slug)
		else:
			if self.request.user.is_superuser or self.request.user.is_staff:
				return Organization.objects.all()
			if self.request.user.is_authenticated():
				return self.request.user.organization_set.all()
			return []


	def get_context_data(self, **kwargs):
		context = super(ScheduleListView, self).get_context_data(**kwargs)
		context['organization'] = self.object
		return context