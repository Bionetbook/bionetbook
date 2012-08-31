from verbs.baseforms import forms


class MixForm(forms.VerbForm):

    name = "mix"
    slug = "mix"

    duration_in_seconds = forms.IntegerField()
