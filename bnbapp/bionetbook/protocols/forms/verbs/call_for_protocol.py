from protocols import forms


class CallForProtocolForm(forms.VerbForm):

    name = "Call For Protocol"
    slug = "call-for-protocol"

    duration_in_seconds = forms.IntegerField()
    edit_protocol_type = forms.CharField()
    edit_input = forms.CharField()
    edit_protocol_output = forms.CharField()
    edit_remarks = forms.CharField()
    min_time = forms.IntegerField()
    max_time = forms.IntegerField()
