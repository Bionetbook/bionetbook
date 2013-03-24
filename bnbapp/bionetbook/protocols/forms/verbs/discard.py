from protocols.forms import forms


class DiscardForm(forms.VerbForm):

    name = "Discard"
    slug = "discard"

    what_are_you_discarding = forms.CharField()
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    remarks = forms.CharField(required = False)
