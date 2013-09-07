from django import forms
from experiment.models import Experiment
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _

class ExperimentForm(forms.ModelForm):

	class Meta:

		model = Experiment
		exclude = ('user', 'data', 'slug', 'owner')

