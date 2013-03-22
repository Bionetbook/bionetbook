from protocols.forms import forms


class ConnectForm(forms.VerbForm):

    name = "Connect"
    slug = "connect"


    edit_to_what = forms.CharField(required = False, help_text = 'sample, mastermix, tube, etc')
    describe_where = forms.CharField(required = False, help_text = 'bench, desktop, rotator, etc')
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    comment_why = forms.CharField(required = False)
    remarks = forms.CharField(required = False)
    using_what = forms.CharField(required = False, help_text = 'rotator, shaker, manual etc')