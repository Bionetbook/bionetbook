from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS


class AddForm(forms.VerbForm):

    name = "Add"  # cannot silence the name without an error, the name here is redundant
    slug = "add"
    has_component = True

    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    max_temp = forms.IntegerField(required = False)
    temp_units = forms.ChoiceField(choices = TEMPERATURE_UNITS, initial = 's')
    # vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    # duration = forms.IntegerField(help_text='this is the minimal time this should take')
    # add_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
