from protocols.forms import forms
from core.utils import VESSELS

class ExtractForm(forms.VerbForm):

    name = "Extract"
    slug = "extract"

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    extracting_from = forms.CharField()
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    comment_why = forms.CharField(required = False)
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
