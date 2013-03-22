from protocols.forms import forms


class AttachForm(forms.VerbForm):

    name = "Attach"
    slug = "attach"

    comment_why = forms.CharField(required = False)
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take')
    remarks = forms.CharField(required = False)