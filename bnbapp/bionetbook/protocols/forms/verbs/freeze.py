from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS
from core.utils import TIME_UNITS

class FreezeForm(forms.VerbForm):

    name = "Freeze"
    slug = "freeze"
    has_machine = True
    layers = ['settify']

    

   