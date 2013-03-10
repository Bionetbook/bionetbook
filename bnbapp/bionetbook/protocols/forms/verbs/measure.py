from protocols.forms import forms


class MeasureForm(forms.VerbForm):

    name = "Measure"
    slug = "measure"
    has_machine = True

    duration_in_seconds = forms.IntegerField()
