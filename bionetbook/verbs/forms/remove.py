from verbs.baseforms import forms


class RemoveForm(forms.VerbForm):

    name = "remove"
    slug = "remove"

    duration_in_seconds = forms.IntegerField()
