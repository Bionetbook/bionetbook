from verbs.baseforms import forms


class CallForProtocolForm(forms.VerbForm):

    name = "call for protocol"
    slug = "call-for-protocol"

    duration_in_seconds = forms.IntegerField()
