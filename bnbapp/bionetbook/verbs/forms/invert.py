from verbs.baseforms import forms


class InvertForm(forms.VerbForm):

    name = "invert"
    slug = "invert"

    duration_in_seconds = forms.IntegerField()
