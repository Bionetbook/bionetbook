from verbs.baseforms import forms


class AliquotForm(forms.VerbForm):

    name = "aliquot"
    slug = "aliquot"

    duration_in_seconds = forms.IntegerField()
