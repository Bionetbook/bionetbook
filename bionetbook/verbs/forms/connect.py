from verbs.baseforms import forms


class ConnectForm(forms.VerbForm):

    name = "connect"
    slug = "connect"


    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()