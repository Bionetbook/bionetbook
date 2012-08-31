from verbs.baseforms import forms


class VortexForm(forms.VerbForm):

    name = "vortex"
    slug = "vortex"

    duration_in_seconds = forms.IntegerField()
