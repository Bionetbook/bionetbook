from verbs.baseforms import forms


class WithdrawForm(forms.VerbForm):

    name = "withdraw"
    slug = "withdraw"

    duration_in_seconds = forms.IntegerField()
