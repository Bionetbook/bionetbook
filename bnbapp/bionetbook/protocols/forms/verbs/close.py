from protocols.forms import forms


class CloseForm(forms.VerbForm):

    name = "Close"
    slug = "close"

    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')