from verbs.baseforms import forms


class DigestForm(forms.VerbForm):

    name = "digest"
    slug = "digest"

    duration_in_seconds = forms.IntegerField()
