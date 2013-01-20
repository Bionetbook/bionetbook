from protocols.forms import forms


class ThawForm(forms.VerbForm):

    name = "Thaw"
    slug = "thaw"
    has_machines = True

    duration_in_seconds = forms.IntegerField()
