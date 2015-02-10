from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS, VESSELS

class CombineForm(forms.VerbForm):

    name = "Combine"
    slug = "combine"
    has_component = True

    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    