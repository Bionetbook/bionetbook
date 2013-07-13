from protocols.forms import forms
from core.utils import VOLUME_UNITS

class LoadForm(forms.VerbForm):

    name = "Load"
    slug = "load"
    has_manual=True
    layers = ['item_to_act','settify', 'conditional_statement']

    item_to_act = forms.CharField(label='what are you loading')
    target = forms.CharField(required=False, help_text='where are you loading it')
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
    conditional_statement = forms.CharField(required=False)
    