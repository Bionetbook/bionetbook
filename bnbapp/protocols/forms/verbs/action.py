from protocols.forms import forms
from core.utils import VESSELS, TIME_UNITS


class ActionForm(forms.VerbForm):

    name = "Action" # cannot silence the name without an error, the name here is redundant
    slug = "action"
    has_manual = True
    layers = ['item_to_act', 'number_of_times', 'settify']

    item_to_act = forms.CharField(help_text = 'what are you doing the action on?')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    number_of_times = forms.IntegerField(required = False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)