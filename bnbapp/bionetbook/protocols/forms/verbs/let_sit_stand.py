from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS, TIME_UNITS

class LetSitStandForm(forms.VerbForm):

    name = "Let Sit/Stand"
    slug = "let-sit-stand"
    has_manual = True

    min_temp = forms.FloatField(required=False)#, initial = 22.0)
    max_temp = forms.FloatField(required=False)#, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    temp_comment = forms.CharField(required=False)
    # min_time = forms.FloatField(required=False)
    # max_time = forms.FloatField(required=False)
    # time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    # time_comment = forms.CharField(required=False)
    
