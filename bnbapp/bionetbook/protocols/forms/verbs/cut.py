from protocols.forms import forms
from core.utils import TIME_UNITS

class CutForm(forms.VerbForm):

    name = "Cut"
    slug = "cut"
    has_manual = True
    layers =['item_to_act', 'target', 'specify_tool','conditional_statement','settify']

    item_to_act = forms.CharField(required=False, help_text='what are you cutting', label='item to remove')
    target = forms.CharField(required=False, help_text='where are you placing it')
    conditional_statement = forms.CharField(required=False)
    specify_tool = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)