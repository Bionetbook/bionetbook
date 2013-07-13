from protocols.forms import forms
from core.utils import VESSELS


class ActionForm(forms.VerbForm):

    name = "Action" # cannot silence the name without an error, the name here is redundant
    slug = "action"
    has_manual = True
    layers = ['item_to_act', 'number_of_times', 'settify']

    item_to_act = forms.CharField(help_text = 'what are you doing the action on?')
    vessel_type = forms.ChoiceField(required = False, choices = VESSELS)
    number_of_times = forms.IntegerField(required = False)
    