from protocols.forms import forms
from core.utils import VESSELS


class ActionForm(forms.VerbForm):

    name = "Action" # cannot silence the name without an error, the name here is redundant
    slug = "action"

    duration = forms.IntegerField(help_text='this is the minimal time this should take')
    comment_why = forms.CharField(required = False)
    apply_action_to = forms.CharField(help_text = 'what are you doing the action on?')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    number_of_times = forms.IntegerField(required = False)
    remarks = forms.CharField(required = False)