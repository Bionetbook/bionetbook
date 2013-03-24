from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS

class LetSitStandForm(forms.VerbForm):

    name = "Let Sit/Stand"
    slug = "let-sit-stand"

    min_temp = forms.FloatField(required=False)#, initial = 22.0)
    max_temp = forms.FloatField(required=False)#, initial = 22.0)
    temp_units = forms.ChoiceField(required=False, choices=TEMPERATURE_UNITS, help_text='in celcius')
    temp_comment = forms.CharField(required=False)
    
