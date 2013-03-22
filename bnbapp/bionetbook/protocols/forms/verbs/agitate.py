from protocols.forms import forms


class AgitateForm(forms.VerbForm):

    name = "Agitate"
    slug = "agitate"
    has_machine = True


    # duration = forms.IntegerField(help_text='this is the minimal time this should take')
    conditional_statement = forms.CharField(required = False, help_text = 'If X, do Y')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, tube, etc')
    comment_why = forms.CharField(required = False, help_text = 'purpose')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')
