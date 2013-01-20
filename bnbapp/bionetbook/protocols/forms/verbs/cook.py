from protocols.forms import forms


class CookForm(forms.VerbForm):

    name = "Cook"
    slug = "cook"
    has_machines = True

    duration_in_seconds = forms.IntegerField()
    temperature = forms.IntegerField()
