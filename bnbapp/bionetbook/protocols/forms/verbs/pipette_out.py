from protocols.forms import forms
from core.utils import VOLUME_UNITS 

class PipetteOutForm(forms.VerbForm):

    name = "Pipette Out"
    slug = "pipette-out"

    has_manual = True
    layers = ['item_to_act','target','conditional_statement','settify']

    item_to_act = forms.CharField(required=False, label='item to pipette_out')
    target = forms.CharField(required=False, help_text='where are you pipetting it to')
    conditional_statement = forms.CharField(required=False)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
