from verbs.baseforms import forms


class RinseForm(forms.VerbForm):

    name = "rinse"
    slug = "rinse"

    duration_in_seconds = forms.IntegerField()
