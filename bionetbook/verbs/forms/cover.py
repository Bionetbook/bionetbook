from verbs.baseforms import forms


class CoverForm(forms.VerbForm):

    name = "cover"
    slug = "cover"

    duration_in_seconds = forms.IntegerField()
