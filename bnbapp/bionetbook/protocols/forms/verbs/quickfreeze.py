from protocols.forms import forms
from core.utils import TEMPERATURE_UNITS

class QuickFreezeForm(forms.VerbForm):

    name = "QuickFreeze"
    slug = "quickfreeze"
    has_manual = True
    layers = ['settify']

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    