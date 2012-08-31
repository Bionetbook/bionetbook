from verbs.baseforms import forms


class ExtractForm(forms.VerbForm):

    name = "extract"
    slug = "extract"

    duration_in_seconds = forms.IntegerField()
