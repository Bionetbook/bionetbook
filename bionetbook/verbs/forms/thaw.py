from verbs.baseforms import forms


class ThawForm(forms.VerbForm):

    name = "thaw"
    slug = "thaw"

    duration_in_seconds = forms.IntegerField()
