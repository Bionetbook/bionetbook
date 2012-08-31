from verbs.baseforms import forms


class PassForm(forms.VerbForm):

    name = "pass"
    slug = "pass"

    duration_in_seconds = forms.IntegerField()
