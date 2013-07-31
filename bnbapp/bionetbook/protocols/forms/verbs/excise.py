from protocols.forms import forms
from core.utils import TIME_UNITS

class ExciseForm(forms.VerbForm):

    name = "Excise"
    slug = "excise"
    has_manual = True
    layers = ['item_to_act','target','using_what','settify']

    item_to_act = forms.CharField(label='what are you exising')
    target = forms.CharField(required=False, help_text='where are you exising into')
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds' )
    time_comment = forms.CharField(required=False)
    
    
