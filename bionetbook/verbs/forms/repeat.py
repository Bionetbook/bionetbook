from verbs.baseforms import forms


class RepeatForm(forms.VerbForm):

    name = "repeat"
    slug = "repeat"

    duration_in_seconds = forms.IntegerField()
