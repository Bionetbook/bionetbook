from verbs.baseforms import forms


class ExciseForm(forms.VerbForm):

    name = "excise"
    slug = "excise"

    duration_in_seconds = forms.IntegerField()
