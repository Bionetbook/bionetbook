from verbs.baseforms import forms


class SuspendForm(forms.VerbForm):

    name = "Suspend"
    slug = "Suspend"


    duration_min_time = forms.IntegerField()