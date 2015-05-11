from protocols.forms import forms
from core.utils import TIME_UNITS

class MixForm(forms.VerbForm):

    name = "Mix"
    slug = "mix"
    has_manual = True
    layers = ['settify']

    min_time = forms.FloatField(required=False, help_text='this is the minimal time this should take', widget=forms.NumberInput(attrs={'step':'any'}))
    max_time = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'step':'any'}))
    time_units = forms.ChoiceField(required=False, choices=TIME_UNITS, help_text='in seconds', initial = 'sec' )
    time_comment = forms.CharField(required=False)
    # duration_min_time = forms.IntegerField()
    # comment_why = forms.CharField()
    # edit_remarks = forms.CharField()
