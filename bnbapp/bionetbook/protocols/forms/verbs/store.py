from protocols.forms import forms
from core.utils import TIME_UNITS

class StoreForm(forms.VerbForm):

    name = "Store"
    slug = "store"

    min_temp = forms.IntegerField(required=False)
    max_temp = forms.IntegerField(required=False)
    time = forms.IntegerField(help_text='how long can it stay there?', required = False)
    time_units = forms.ChoiceField(choices = TIME_UNITS)
