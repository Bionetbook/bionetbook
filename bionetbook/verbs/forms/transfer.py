from verbs.baseforms import forms


class TransferForm(forms.VerbForm):

    name = "transfer"
    slug = "transfer"

    duration_in_seconds = forms.IntegerField()
