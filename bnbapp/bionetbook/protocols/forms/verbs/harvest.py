from verbs.baseforms import forms


class HarvestForm(forms.VerbForm):

    name = "harvest"
    slug = "harvest"

    duration_in_seconds = forms.IntegerField()
