from verbs.baseforms import forms


class CentrifugeForm(forms.VerbForm):

    name = "centrifuge"
    slug = "centrifuge"

    duration_in_seconds = forms.IntegerField()
    speed_in_rcf = forms.IntegerField()
    temperature = forms.IntegerField()
