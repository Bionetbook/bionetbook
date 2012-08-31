from verbs.baseforms import forms


class PlaceForm(forms.VerbForm):

    name = "place"
    slug = "place"

    duration_in_seconds = forms.IntegerField()
