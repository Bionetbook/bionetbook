from verbs.baseforms import forms


class ThermalCycleForm(forms.VerbForm):

    name = "thermal cycle"
    slug = "thermal-cycle"

    duration_in_seconds = forms.IntegerField()
