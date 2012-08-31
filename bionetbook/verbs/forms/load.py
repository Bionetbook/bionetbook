from verbs.baseforms import forms


class LoadForm(forms.VerbForm):

    name = "load"
    slug = "load"

    duration_in_seconds = forms.IntegerField()
