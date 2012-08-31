from verbs.baseforms import forms


class StoreForm(forms.VerbForm):

    name = "store"
    slug = "store"

    duration_in_seconds = forms.IntegerField()
