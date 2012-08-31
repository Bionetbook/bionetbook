from verbs.baseforms import forms


class DryForm(forms.VerbForm):

    name = "dry"
    slug = "dry"

    duration_in_seconds = forms.IntegerField()
