from verbs.baseforms import forms


class EluteForm(forms.VerbForm):

    name = "elute"
    slug = "elute"

    duration_in_seconds = forms.IntegerField()
