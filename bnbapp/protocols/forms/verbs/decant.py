from protocols.forms import forms
from core.utils import TIME_UNITS

class DecantForm(forms.VerbForm):

    name = "Decant"
    slug = "decant"
    has_manual = True
    layer= ['item_to_act', 'target', 'settify']
    
    item_to_act = forms.CharField(required=False, label='item to decant')
    target = forms.CharField(required=False, help_text='where are you placing it')
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)