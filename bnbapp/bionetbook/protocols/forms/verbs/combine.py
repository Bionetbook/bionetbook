from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS, VESSELS

class CombineForm(forms.VerbForm):

    name = "Combine"
    slug = "combine"
    has_component = True


    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField(required = False)
    temp_units = forms.ChoiceField(choices = TEMPERATURE_UNITS, initial = 's')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    