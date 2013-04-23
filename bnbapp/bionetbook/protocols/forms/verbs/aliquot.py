from protocols.forms import forms
from core.utils import  VOLUME_UNITS, CONCENTRATION_UNITS, VESSELS


class AliquotForm(forms.VerbForm):

    name = "Aliquot"
    slug = "aliquot"
    has_manual = True
    layers = ['item_to_act','number_of_aliquots','aliquot_vol','vol_units','aliquot_conc','conc_units','technical_comment','duration','duration_units']

    item_to_act = forms.CharField(required=False, label='item to aliquot')
    vessel_type = forms.ChoiceField(choices = VESSELS)
    batch_size = forms.IntegerField(help_text = 'number of tubes you are aliquoting into', label='number of aliquots', required =False)
    aliquot_vol = forms.IntegerField(required=False)
    vol_units = forms.ChoiceField(choices = VOLUME_UNITS)
    aliquot_conc = forms.IntegerField(required=False)
    conc_units = forms.ChoiceField(required=False, choices = CONCENTRATION_UNITS)

    
