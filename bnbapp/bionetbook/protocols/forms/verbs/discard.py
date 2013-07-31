from protocols.forms import forms
from core.utils import TIME_UNITS

class DiscardForm(forms.VerbForm):

    name = "Discard"
    slug = "discard"
    has_manual = True
    layers = ['item_to_act','item_to_retain','conditional_statement','settify']

    item_to_act = forms.CharField(required=False, label='item to discard')
    item_to_retain = forms.CharField()
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)
