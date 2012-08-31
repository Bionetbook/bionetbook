from verbs.baseforms import forms


class RecoverForm(forms.VerbForm):

    name = "recover"
    slug = "recover"

    duration_in_seconds = forms.IntegerField()
