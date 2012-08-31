from verbs.baseforms import forms


class GrindForm(forms.VerbForm):

    name = "grind"
    slug = "grind"

    duration_in_seconds = forms.IntegerField()
