from protocols.forms import forms
from core.utils import  VOLUME_UNITS, VESSELS

class FilterForm(forms.VerbForm):

    name = "Filter"
    slug = "filter"

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    comment_why = forms.CharField(required = False)
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    volume_units = forms.ChoiceField(choices = VOLUME_UNITS)
    min_vol = forms.FloatField(required=False)
    max_vol = forms.FloatField(required=False)