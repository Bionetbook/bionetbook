from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS, TIME_UNITS

class QuickFreezeForm(forms.VerbForm):

    name = "QuickFreeze"
    slug = "quickfreeze"
    has_manual = True
    layers = ['settify']

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)