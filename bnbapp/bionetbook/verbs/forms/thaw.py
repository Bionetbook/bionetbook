from verbs.baseforms import forms


class ThawForm(forms.VerbForm):

    name = "Thaw"
    slug = "thaw"

    duration_in_seconds = forms.IntegerField()
