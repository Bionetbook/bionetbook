from verbs.baseforms import forms


class ConnectForm(forms.VerbForm):

    name = "connect"
    slug = "connect"

    duration_in_seconds = forms.IntegerField()
