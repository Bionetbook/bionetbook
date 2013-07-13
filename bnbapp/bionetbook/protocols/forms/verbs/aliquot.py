from protocols.forms import forms
from core.utils import  VOLUME_UNITS, CONCENTRATION_UNITS, VESSELS, TIME_UNITS


class AliquotForm(forms.VerbForm):

    name = "Aliquot"
    slug = "aliquot"
    has_manual = True
    layers = ['item_to_act','number_of_aliquots','settify']

    item_to_act = forms.CharField(required=False, label='item to aliquot')
    vessel_type = forms.ChoiceField(choices = VESSELS)
    batch_size = forms.IntegerField(help_text = 'number of tubes you are aliquoting into', label='number of aliquots', required =False)
    min_conc = forms.FloatField(required=False)
    max_conc = forms.FloatField(required=False)
    conc_units = forms.ChoiceField(required=False, choices=CONCENTRATION_UNITS )
    conc_comment = forms.CharField(required=False)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)

    
