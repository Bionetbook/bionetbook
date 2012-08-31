from verbs.baseforms import forms


class ApplyForm(forms.VerbForm):

    name = "apply"
    slug = "apply"

    duration_in_seconds = forms.IntegerField()
