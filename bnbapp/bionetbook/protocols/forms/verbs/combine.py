from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS, VESSELS

class CombineForm(forms.VerbForm):

    name = "Combine"
    slug = "combine"
    has_component = True

    max_temp = forms.IntegerField(required = False)
    temp_units = forms.ChoiceField(choices = TEMPERATURE_UNITS, initial = 's')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    