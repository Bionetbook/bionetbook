from verbs.baseforms import forms


class GrowForm(forms.VerbForm):

    name = "grow"
    slug = "grow"

    duration_in_seconds = forms.IntegerField()
