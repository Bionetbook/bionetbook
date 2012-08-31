from verbs.baseforms import forms


class SplitForm(forms.VerbForm):

    name = "split"
    slug = "split"

    duration_in_seconds = forms.IntegerField()
