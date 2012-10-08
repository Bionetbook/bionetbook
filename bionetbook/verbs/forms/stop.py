from verbs.baseforms import forms


class StopForm(forms.VerbForm):

    name = "stop"
    slug = "stop"


    Edit_what_remark=forms.CharField()
    Duration_Min_Time=forms.IntegerField()
    Specify_tool=forms.CharField()
    Edit_kit_name=forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()
    Edit_vessel_type=forms.CharField()
    Describe_where=forms.CharField()