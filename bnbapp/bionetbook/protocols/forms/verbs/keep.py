from protocols import forms


class KeepForm(forms.VerbForm):

    name = "keep"
    slug = "keep"

    duration_in_seconds = forms.IntegerField()
