from protocols import forms


class PcrForm(forms.VerbForm):

    name = "PCR"
    slug = "pcr"

    duration_in_seconds = forms.IntegerField()
