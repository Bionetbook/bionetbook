from verbs.baseforms import forms


class DigestForm(forms.VerbForm):

    name = "Digest"
    slug = "digest"

    duration_in_seconds = forms.IntegerField()
