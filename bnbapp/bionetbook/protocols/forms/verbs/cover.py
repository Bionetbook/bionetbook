from protocols.forms import forms


class CoverForm(forms.VerbForm):

    name = "Cover"
    slug = "cover"


    conditional_statement = forms.CharField(required = False, help_text ='if X happens, do Y')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    remarks = forms.CharField(required = False)