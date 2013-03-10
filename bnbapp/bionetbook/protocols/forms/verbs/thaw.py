from protocols.forms import forms


class ThawForm(forms.VerbForm):

    name = "Thaw"
    slug = "thaw"
    has_machine = True

    duration_in_seconds = forms.IntegerField()
