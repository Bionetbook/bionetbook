from protocols.forms import forms


class VisualizeForm(forms.VerbForm):

    name = "Visualize"
    slug = "visualize"

    duration_in_seconds = forms.IntegerField()
