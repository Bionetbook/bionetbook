from protocols.forms import forms
from core.utils import VESSELS, TIME_UNITS


class FollowInstructionsForm(forms.VerbForm):

    name = "Follow instructions" # cannot silence the name without an error, the name here is redundant
    slug = "follow_instructions"
    has_manual = True
    layers = ['source', 'input_to_track', 'output_to_track', 'settify']

    source = forms.CharField(required = False, help_text = 'document refered to')
    input_to_track = forms.CharField(required = False, help_text = 'reagent, sample, molecule, compounds, strain etc.')
    input_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    output_to_track = forms.CharField(required = False, help_text = 'reagent, sample, molecule, compounds, strain etc.')
    output_notes = forms.CharField(required = False, help_text = 'concentration, volume, mass etc')
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)