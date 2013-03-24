from protocols.forms import forms


class DryForm(forms.VerbForm):

    name = "Dry"
    slug = "dry"
    has_machine = True

    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)