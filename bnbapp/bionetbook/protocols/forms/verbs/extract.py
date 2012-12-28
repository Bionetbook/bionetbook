from protocols.forms import forms


class ExtractForm(forms.VerbForm):

    name = "Extract"
    slug = "extract"

    duration_in_seconds = forms.IntegerField()
