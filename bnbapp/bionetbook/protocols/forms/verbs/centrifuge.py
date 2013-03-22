from protocols.forms import forms
from core.utils import SPEED_UNITS

class CentrifugeForm(forms.VerbForm):

    name = "Centrifuge"
    slug = "centrifuge"
    has_machine = True

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    min_speed = forms.IntegerField()
    max_speed = forms.IntegerField(required = False)
    speed_units = forms.ChoiceField(required=False, choices = SPEED_UNITS, initial = 'rpm' )
    speed_comment = forms.CharField(required=False)
    comment_why = forms.CharField(required = False)