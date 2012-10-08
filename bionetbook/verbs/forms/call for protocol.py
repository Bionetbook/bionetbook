from verbs.baseforms import forms


class CallforprotocolForm(forms.VerbForm):

    name = "callforprotocol"
    slug = "callforprotocol"


    Edit_protocol_type=forms.CharField()
    Edit_input =forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()
    Duration_Min_Time=forms.IntegerField()