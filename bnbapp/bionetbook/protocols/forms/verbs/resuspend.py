from protocols.forms import forms
from core.utils import VOLUME_UNITS, CONCENTRATION_UNITS, TIME_UNITS

class ResuspendForm(forms.VerbForm):

    name = "Resuspend"
    slug = "resuspend"
    # has_component = True
    has_manual = True
    layers = ['item_to_act', 'reagent', 'settify']

    item_to_act = forms.CharField(required=False, help_text='what are you resuspending?', label='item to resuspend')
    reagent = forms.CharField(required=False, help_text='where are you washing it with')
    min_conc = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_conc = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    conc_units = forms.ChoiceField(required=False, choices=CONCENTRATION_UNITS )
    conc_comment = forms.CharField(required=False)
    min_vol = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_vol = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    vol_units = forms.ChoiceField(required=False, choices=VOLUME_UNITS )
    vol_comment = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)

