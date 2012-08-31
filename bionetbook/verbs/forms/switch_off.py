from verbs.baseforms import forms


class SwitchOffForm(forms.VerbForm):

    name = "switch off"
    slug = "switch-off"

    duration_in_seconds = forms.IntegerField()
