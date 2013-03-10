from protocols.forms import forms


class InvertForm(forms.VerbForm):

    name = "Invert"
    slug = "invert"

    duration_in_seconds = forms.IntegerField()
