from protocols.forms import forms


class ApplyForm(forms.VerbForm):

    name = "Apply"
    slug = "apply"

    duration = forms.IntegerField(help_text='this is the minimal time this should take')
    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    remarks = forms.CharField(required = False)
    specify_tool = forms.CharField(required = False, help_text = 'not machine, scissors, pippete, blade etc')
    comment_why = forms.CharField(required = False)
    number_of_times = forms.IntegerField(required = False)