from protocols.forms import forms
from core.utils import   VESSELS

class GrowForm(forms.VerbForm):

    name = "Grow"
    slug = "grow"

    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    remarks = forms.CharField(required = False)
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    comment_why = forms.CharField(required = False)
