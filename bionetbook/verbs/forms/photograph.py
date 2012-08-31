from verbs.baseforms import forms


class PhotographForm(forms.VerbForm):

    name = "photograph"
    slug = "photograph"

    duration_in_seconds = forms.IntegerField()
