from verbs.baseforms import forms


class PurifyForm(forms.VerbForm):

    name = "purify"
    slug = "purify"

    duration_in_seconds = forms.IntegerField()
