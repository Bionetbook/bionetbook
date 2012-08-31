from verbs.baseforms import forms


class VisualizeForm(forms.VerbForm):

    name = "visualize"
    slug = "visualize"

    duration_in_seconds = forms.IntegerField()
