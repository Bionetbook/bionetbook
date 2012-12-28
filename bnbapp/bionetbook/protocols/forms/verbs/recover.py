from protocols.forms import forms


class RecoverForm(forms.VerbForm):

    name = "Recover"
    slug = "recover"

    duration_in_seconds = forms.IntegerField()
