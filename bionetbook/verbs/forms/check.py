from verbs.baseforms import forms


class CheckForm(forms.VerbForm):

    name = "check"
    slug = "check"

    duration_in_seconds = forms.IntegerField()
