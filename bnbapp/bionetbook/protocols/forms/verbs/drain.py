from verbs.baseforms import forms


class DrainForm(forms.VerbForm):

    name = "Drain"
    slug = "drain"

    duration_in_seconds = forms.IntegerField()
