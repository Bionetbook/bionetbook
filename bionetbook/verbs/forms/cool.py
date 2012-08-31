from verbs.baseforms import forms


class CoolForm(forms.VerbForm):

    name = "cool"
    slug = "cool"

    duration_in_seconds = forms.IntegerField()
