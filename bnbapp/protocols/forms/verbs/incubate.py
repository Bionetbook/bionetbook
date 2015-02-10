from protocols.forms import forms


class IncubateForm(forms.VerbForm):

    name = "Incubate"
    slug = "incubate"
    has_machine = True

    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    remarks = forms.CharField(required = False)
    
