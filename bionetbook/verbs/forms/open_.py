from verbs.baseforms import forms


class OpenForm(forms.VerbForm):

    name = "open"
    slug = "open"

    duration_in_seconds = forms.IntegerField()
