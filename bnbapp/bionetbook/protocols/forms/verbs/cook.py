from protocols.forms import forms


class CookForm(forms.VerbForm):

    name = "Cook"
    slug = "cook"
    has_machine = True

    comment_why = forms.CharField(required = False)
    # duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    remarks = forms.CharField(required = False)
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')	