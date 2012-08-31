from verbs.baseforms import forms


class StopForm(forms.VerbForm):

    name = "stop"
    slug = "stop"

    duration_in_seconds = forms.IntegerField()
