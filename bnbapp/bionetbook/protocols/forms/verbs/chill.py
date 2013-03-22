from protocols.forms import forms


class ChillForm(forms.VerbForm):

    name = "Chill"
    slug = "chill"
    has_machine = True

    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    remarks = forms.CharField(required = False)
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    comment_why = forms.CharField(required = False)
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')