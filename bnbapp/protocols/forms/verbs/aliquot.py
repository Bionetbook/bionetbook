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
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)
    
