from verbs.baseforms import forms


class DiscardForm(forms.VerbForm):

    name = "discard"
    slug = "discard"

    duration_in_seconds = forms.IntegerField()
