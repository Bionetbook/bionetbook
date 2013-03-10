from protocols.forms import forms


class HarvestForm(forms.VerbForm):

    name = "Harvest"
    slug = "harvest"

    duration_in_seconds = forms.IntegerField()
