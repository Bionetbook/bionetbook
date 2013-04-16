from protocols.forms import forms


class DryForm(forms.VerbForm):

    name = "Dry"
    slug = "dry"
    has_manual = True

    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    remarks = forms.CharField(required = False)