from django import forms
from experiment.models import Experiment
from workflow.models import Workflow
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class ExperimentForm(forms.ModelForm):

	class Meta:

		model = Experiment
		exclude = ('user', 'data', 'slug', 'owner')

class ExperimentManualForm(forms.Form):
    # name = forms.CharField( widget=forms.TextInput(attrs={'class':'special'}) )
    name = forms.CharField( widget=forms.TextInput() )
    workflows = forms.ModelChoiceField(required=False, queryset=EmptyQuerySet(), label=_("Workflows"))
    
    # UPDATE IT IN THE VIEW
    # form.fields['protocols'] = forms.ModelChoiceField( queryset=self.request.user.profile.get_published_protocols_qs(), label=_("Protocol"), widget=forms.CheckboxSelectMultiple() )

class ExperimentAddForm(forms.Form):
	calendars = forms.ModelChoiceField(required=False, queryset=EmptyQuerySet(), label=_("Calendars"))