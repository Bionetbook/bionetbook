from verbs.baseforms import forms


class CollectForm(forms.VerbForm):

    name = "collect"
    slug = "collect"

    duration_in_seconds = forms.IntegerField()
