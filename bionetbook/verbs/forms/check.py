from verbs.baseforms import forms


class CheckForm(forms.VerbForm):

    name = "check"
    slug = "check"


    Edit_what_remark=forms.CharField()
    Specify_machine=forms.CharField()
    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_protocol_output=forms.CharField()
    Specify_tool=forms.CharField()