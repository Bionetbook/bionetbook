from protocols.forms import forms
from core.utils import TIME_UNITS, TEMPERATURE_UNITS

class StoreForm(forms.VerbForm):

    name = "Store"
    slug = "store"
    has_manual = True
    layers = ["item_to_act", 'settify']
    
    item_to_act = forms.CharField(required=False, help_text='what are you removing', label='item to remove')
