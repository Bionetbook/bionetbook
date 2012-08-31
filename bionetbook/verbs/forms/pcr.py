from verbs.baseforms import forms


class PcrForm(forms.VerbForm):

    name = "pcr"
    slug = "pcr"

    duration_in_seconds = forms.IntegerField()
