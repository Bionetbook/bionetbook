from verbs.baseforms import forms


class MicrocentrifugeForm(forms.VerbForm):

    name = "microcentrifuge"
    slug = "microcentrifuge"

    duration_in_seconds = forms.IntegerField()
