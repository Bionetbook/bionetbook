from verbs.baseforms import forms


class ElectrophoreseForm(forms.VerbForm):

    name = "electrophorese"
    slug = "electrophorese"

    duration_in_seconds = forms.IntegerField()
