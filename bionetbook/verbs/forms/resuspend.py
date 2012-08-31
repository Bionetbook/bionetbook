from verbs.baseforms import forms


class ResuspendForm(forms.VerbForm):

    name = "resuspend"
    slug = "resuspend"

    duration_in_seconds = forms.IntegerField()
