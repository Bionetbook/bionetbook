from verbs.baseforms import forms


class ShakeForm(forms.VerbForm):

    name = "shake"
    slug = "shake"

    duration_in_seconds = forms.IntegerField()
