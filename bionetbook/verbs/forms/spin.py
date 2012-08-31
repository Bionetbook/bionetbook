from verbs.baseforms import forms


class SpinForm(forms.VerbForm):

    name = "spin"
    slug = "spin"

    duration_in_seconds = forms.IntegerField()
