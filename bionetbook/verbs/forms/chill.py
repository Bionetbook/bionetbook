from verbs.baseforms import forms


class ChillForm(forms.VerbForm):

    name = "chill"
    slug = "chill"

    duration_in_seconds = forms.IntegerField()
