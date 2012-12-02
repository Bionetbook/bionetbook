from verbs.baseforms import forms


class PurifyForm(forms.VerbForm):

    name = "Purify"
    slug = "purify"

    duration_in_seconds = forms.IntegerField()
