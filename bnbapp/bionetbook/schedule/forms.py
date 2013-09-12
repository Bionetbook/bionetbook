from django import forms
from schedule.models import Calendar
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class CalendarForm(forms.ModelForm):

	class Meta:

		model = Calendar
		exclude = ('user', 'data', 'slug')

class CalendarManualForm(forms.Form):
	name = forms.CharField( widget=forms.TextInput() )