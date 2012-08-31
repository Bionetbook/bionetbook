from verbs.baseforms import forms


class DecantForm(forms.VerbForm):

    name = "decant"
    slug = "decant"

    duration_in_seconds = forms.IntegerField()
