from verbs.baseforms import forms


class CloseForm(forms.VerbForm):

    name = "close"
    slug = "close"

    duration_in_seconds = forms.IntegerField()
