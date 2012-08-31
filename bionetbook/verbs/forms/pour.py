from verbs.baseforms import forms


class PourForm(forms.VerbForm):

    name = "pour"
    slug = "pour"

    duration_in_seconds = forms.IntegerField()
