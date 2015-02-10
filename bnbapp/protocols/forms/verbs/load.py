from protocols.forms import forms
from core.utils import VOLUME_UNITS, TIME_UNITS

class LoadForm(forms.VerbForm):

    name = "Load"
    slug = "load"
    has_manual=True
    layers = ['item_to_act', 'conditional_statement','settify']

    item_to_act = forms.CharField(label='what are you loading')
    target = forms.CharField(required=False, help_text='where are you loading it')
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
    conditional_statement = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)
    