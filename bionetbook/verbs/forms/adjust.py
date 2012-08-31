from verbs.baseforms import forms


class AdjustForm(forms.VerbForm):

    name = "adjust"
    slug = "adjust"

    duration_in_seconds = forms.IntegerField()
