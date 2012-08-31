from verbs.baseforms import forms


class PipetteOutForm(forms.VerbForm):

    name = "pipette out"
    slug = "pipette-out"

    duration_in_seconds = forms.IntegerField()
