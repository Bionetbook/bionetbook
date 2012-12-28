from protocols import forms


class ConnectForm(forms.VerbForm):

    name = "Connect"
    slug = "connect"


    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()