from verbs.baseforms import forms


class SpinForm(forms.VerbForm):

    name = "Spin"
    slug = "spin"

    duration_in_seconds = forms.IntegerField()
