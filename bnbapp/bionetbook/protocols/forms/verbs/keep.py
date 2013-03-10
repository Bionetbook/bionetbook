from protocols.forms import forms


class KeepForm(forms.VerbForm):

    name = "Keep"
    slug = "keep"

    duration_in_seconds = forms.IntegerField()
