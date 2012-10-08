from verbs.baseforms import forms


class ExciseForm(forms.VerbForm):

    name = "excise"
    slug = "excise"


    Edit_what_remark=forms.CharField()
    Specify_tool=forms.CharField()
    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Edit_kit_name=forms.CharField()
    Edit_protocol_output=forms.CharField()