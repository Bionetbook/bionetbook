from protocols.forms import forms


class SuspendForm(forms.VerbForm):

    name = "Suspend"
    slug = "suspend"

    duration_min_time = forms.IntegerField()