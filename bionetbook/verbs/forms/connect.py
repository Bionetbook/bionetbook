from verbs.baseforms import forms


class ConnectForm(forms.VerbForm):

    name = "connect"
    slug = "connect"


    Edit_what_remark=forms.CharField()
    Describe_where=forms.CharField()
    Duration_Min_Time=forms.IntegerField()