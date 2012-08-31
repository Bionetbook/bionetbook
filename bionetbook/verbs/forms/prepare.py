from verbs.baseforms import forms


class PrepareForm(forms.VerbForm):

    name = "prepare"
    slug = "prepare"

    duration_in_seconds = forms.IntegerField()
