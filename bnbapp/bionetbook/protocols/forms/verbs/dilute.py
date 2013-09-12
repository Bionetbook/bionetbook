from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS


class DiluteForm(forms.VerbForm):

    name = "Dilute"  # cannot silence the name without an error, the name here is redundant
    slug = "dilute"
    has_component = True

    # conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
	    


