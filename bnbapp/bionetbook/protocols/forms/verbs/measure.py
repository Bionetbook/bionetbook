from protocols.forms import forms


class MeasureForm(forms.VerbForm):

    name = "measure"
    slug = "measure"

    duration_in_seconds = forms.IntegerField()
