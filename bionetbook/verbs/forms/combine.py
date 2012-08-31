from verbs.baseforms import forms


class CombineForm(forms.VerbForm):

    name = "combine"
    slug = "combine"

    duration_in_seconds = forms.IntegerField()
