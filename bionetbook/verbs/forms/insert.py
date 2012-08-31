from verbs.baseforms import forms


class InsertForm(forms.VerbForm):

    name = "insert"
    slug = "insert"

    duration_in_seconds = forms.IntegerField()
