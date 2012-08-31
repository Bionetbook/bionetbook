from verbs.baseforms import forms


class IncubateForm(forms.VerbForm):

    name = "incubate"
    slug = "incubate"

    duration_in_seconds = forms.IntegerField()
