from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS

class QuickFreezeForm(forms.VerbForm):

    name = "QuickFreeze"
    slug = "quickfreeze"
    has_manual = True

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    min_temp = forms.min_temp = forms.FloatField(required=False)#, initial = 22.0)
    max_temp = forms.FloatField(required=False)#, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    temp_comment = forms.CharField(required=False)