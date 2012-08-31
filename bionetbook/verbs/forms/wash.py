from verbs.baseforms import forms


class WashForm(forms.VerbForm):

    name = "wash"
    slug = "wash"

    duration_in_seconds = forms.IntegerField()
