from verbs.baseforms import forms


class HeatForm(forms.VerbForm):

    name = "heat"
    slug = "heat"

    duration_in_seconds = forms.IntegerField()
