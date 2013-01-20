from protocols.forms import forms


class SpinForm(forms.VerbForm):

    name = "Spin"
    slug = "spin"
    has_machines = True

    duration_in_seconds = forms.IntegerField()
