from verbs.baseforms import forms


class MeltForm(forms.VerbForm):

    name = "melt"
    slug = "melt"

    duration_in_seconds = forms.IntegerField()
