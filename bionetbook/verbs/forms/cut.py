from verbs.baseforms import forms


class CutForm(forms.VerbForm):

    name = "cut"
    slug = "cut"

    duration_in_seconds = forms.IntegerField()
