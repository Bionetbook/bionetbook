from protocols.forms import forms


class CollectForm(forms.VerbForm):

    name = "Collect"
    slug = "collect"
    has_machines = True

    duration_in_seconds = forms.IntegerField()
