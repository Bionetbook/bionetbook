from verbs.baseforms import forms


class WeighForm(forms.VerbForm):

    name = "weigh"
    slug = "weigh"

    duration_in_seconds = forms.IntegerField()
