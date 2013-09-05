from protocols.forms import forms
from core.utils import TIME_UNITS

class RepeatForm(forms.VerbForm):

    name = "Repeat"
    slug = "repeat"
    has_manual = True
    layer=['item_to_act', 'number_of_times','conditonal_stetement' 'settify']

    item_to_act = forms.CharField(required=False, help_text='from what step are you repeating?', label='item to repeat')
    number_of_times = forms.IntegerField(required = False)
    conditional_statement = forms.CharField(required=False)
    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)