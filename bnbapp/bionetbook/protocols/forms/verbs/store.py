from protocols.forms import forms
from core.utils import TIME_UNITS, TEMPERATURE_UNITS

class StoreForm(forms.VerbForm):

    name = "Store"
    slug = "store"
    has_manual = True
    layers = ['settify']
    
    min_temp = forms.IntegerField(required=False)
    max_temp = forms.IntegerField(required=False)
    temp_units = forms.ChoiceField(choices = TEMPERATURE_UNITS, initial='C')
    # time = forms.IntegerField(help_text='how long can it stay there?', required = False)
    # time_units = forms.ChoiceField(choices = TIME_UNITS)
