from protocols import forms


class MicrocentrifugeForm(forms.VerbForm):

    name = "Microcentrifuge"
    slug = "microcentrifuge"

    duration_in_seconds = forms.IntegerField()
