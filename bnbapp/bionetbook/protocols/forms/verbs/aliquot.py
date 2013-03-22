from protocols.forms import forms
from core.utils import  VOLUME_UNITS, CONCENTRATION_UNITS, VESSELS


class AliquotForm(forms.VerbForm):

    name = "Aliquot"
    slug = "aliquot"

    duration = forms.IntegerField(help_text = 'minimal time that this will take')
    aliquote_what = forms.CharField(help_text = 'name of reagent or mix')
    vessel_type = forms.ChoiceField(choices = VESSELS)
    number_of_aliquots = forms.IntegerField(help_text = 'number of tubes you are aliquoting into')
    aliquot_volume = forms.IntegerField()
    aliquot_concentration = forms.IntegerField()
    volume_units = forms.ChoiceField(choices = VOLUME_UNITS)
    concentration_units = forms.ChoiceField(choices = CONCENTRATION_UNITS)

    
