from protocols.forms import forms
from core.utils import TIME_UNITS

class PlaceForm(forms.VerbForm):

    name = "Place"
    slug = "place"
    has_manual = True
    layers = ['item_to_act','target','conditional_statement','settify']
    
    item_to_act = forms.CharField(required=False, label='what are you placing')
    target = forms.CharField(required=False, help_text='where are you placing it')
    conditional_statement = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)
'''
place tubes on ice
Place a QIAquick spin column in a provided 2 ml collection tube
Place a QIAquick spin column in a provided 1.5 ml collection tube



'''