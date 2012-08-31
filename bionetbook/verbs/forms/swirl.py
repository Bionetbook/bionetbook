from verbs.baseforms import forms


class SwirlForm(forms.VerbForm):

    name = "swirl"
    slug = "swirl"

    duration_in_seconds = forms.IntegerField()
