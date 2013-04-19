from protocols.forms import forms
from core.utils import VOLUME_UNITS 

class PipetteOutForm(forms.VerbForm):

    name = "Pipette Out"
    slug = "pipette-out"

    has_manual = True
    layers = ['item_to_place','target','conditional_statement','vol','vol_unit','technique_comment','duration','duration_units']

    item_to_place = forms.CharField(required=False, help_text='what are you placing', label='item to pipette-out')
    target = forms.CharField(required=False, help_text='where are you placing it')
    conditional_statement = forms.CharField(required=False)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
