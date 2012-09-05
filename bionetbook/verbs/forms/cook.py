from verbs.baseforms import forms


class CookForm(forms.VerbForm):

    name = "cook"
    slug = "cook"

    duration_in_seconds = forms.IntegerField()
    temperature = forms.IntegerField()
