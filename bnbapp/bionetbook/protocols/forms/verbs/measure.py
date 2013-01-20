from protocols.forms import forms


class MeasureForm(forms.VerbForm):

    name = "measure"
    slug = "measure"
    has_machines = True

    duration_in_seconds = forms.IntegerField()
