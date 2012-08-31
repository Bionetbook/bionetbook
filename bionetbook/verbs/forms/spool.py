from verbs.baseforms import forms


class SpoolForm(forms.VerbForm):

    name = "spool"
    slug = "spool"

    duration_in_seconds = forms.IntegerField()
