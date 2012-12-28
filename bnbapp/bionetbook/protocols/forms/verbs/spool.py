from protocols import forms


class SpoolForm(forms.VerbForm):

    name = "Spool"
    slug = "spool"

    duration_in_seconds = forms.IntegerField()
