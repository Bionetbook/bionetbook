from verbs.baseforms import forms


class SealForm(forms.VerbForm):

    name = "seal"
    slug = "seal"

    duration_in_seconds = forms.IntegerField()
