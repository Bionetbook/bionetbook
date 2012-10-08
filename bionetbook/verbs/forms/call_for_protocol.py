from verbs.baseforms import forms


class CallForProtocolForm(forms.VerbForm):

    name = "call for protocol"
    slug = "call-for-protocol"

    duration_in_seconds = forms.IntegerField()
    Edit_protocol_type=forms.CharField()
    Edit_input =forms.CharField()
    Edit_protocol_output=forms.CharField()
    Edit_remarks=forms.CharField()
    Min_Time=forms.IntegerField()
    Max_Time=forms.IntegerField()